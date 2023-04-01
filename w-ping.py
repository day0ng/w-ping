#!/usr/bin/env python

"""
    A pure python multi-ping program, it's simple and light.

    Copyright (c) Dayong Wang, wandering_997@sina.com
    Distributable under the terms of the GNU General Public License
    version 2. Provided with no warranties of any sort.

    Original Pyhton ping code
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    https://github.com/samuel/python-ping/

    Revision history
    ~~~~~~~~~~~~~~~~
    2023/04/02
    Dayong Wang
    Renew code for Python 3.

    2016/11/02
    Dayong Wang
    Bug fix, low performance while multi-ping. And add short name of some options.

    2016/09/16
    Dayong Wang
    Add Linux ping as default detector instead of pure-python-ping. 

    2016/09/13
    Dayong Wang
    Fix Exception KeyError by moving monkey.patch_all() on the top of import.

    2016/02/20
    Dayong Wang
    Use gevent.

    2016/01/23
    Dayong Wang
    Add multiprocessing function which can be enabled by option --process.

    2016/01/18
    Dayong Wang
    Replace getopt with argparse.

    2015/11/06
    Creates by Dayong Wang (wandering_997@sina.com)

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate: $
    $Rev: $
    $Author: $
"""

import gevent
from gevent import monkey
monkey.patch_all()

import argparse
import logging
import os
import platform
import re
import select
import socket
import struct
import sys
import time
from gevent import subprocess
from gevent.queue import Queue, Empty

tasks = Queue(maxsize=10000)
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# From /usr/include/linux/icmp.h; your milage may vary.
ICMP_ECHO_REQUEST = 8       # Seems to be the same on Solaris.


def sys_cmd(str_cmd):

    sp = subprocess.Popen(str_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    str_out = sp.stdout.read().decode()
    str_err = sp.stderr.read().decode()
    sp.wait()
    return [str_out, str_err]


def checksum(source_string):
    """
    I'm not too confident that this is right but testing seems
    to suggest that it gives the same answers as in_cksum in ping.c
    """
    the_sum = 0
    count_to = (len(source_string)/2)*2
    count = 0
    while count < count_to:
        this_val = ord(source_string[count + 1])*256 + ord(source_string[count])
        the_sum = the_sum + this_val
        the_sum = the_sum & 0xffffffff # Necessary?
        count = count + 2

    if count_to<len(source_string):
        the_sum = the_sum + ord(source_string[len(source_string) - 1])
        the_sum = the_sum & 0xffffffff # Necessary?

    the_sum = (the_sum >> 16)  +  (the_sum & 0xffff)
    the_sum = the_sum + (the_sum >> 16)
    answer = ~the_sum
    answer = answer & 0xffff

    # Swap bytes. Bugger me if I know why.
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def receive_one_ping(my_socket, id, timeout):
    """
    receive the ping from the socket.
    """
    time_left = timeout
    while True:
        started_select = time.time()
        what_ready = select.select([my_socket], [], [], time_left)
        how_long_in_select = (time.time() - started_select)
        if what_ready[0] == []: # Timeout
            return

        time_received = time.time()
        rec_packet, addr = my_socket.recvfrom(1024)
        icmp_header = rec_packet[20:28]
        icmp_type, code, checksum, packet_id, sequence = struct.unpack(
            "bbHHh", icmp_header
        )
        # Filters out the echo request itself. 
        # This can be tested by pinging 127.0.0.1 
        # You'll see your own request
        if icmp_type != 8 and packet_id == id:
            bytes_in_double = struct.calcsize("d")
            time_sent = struct.unpack("d", rec_packet[28:28 + bytes_in_double])[0]
            return time_received - time_sent

        time_left = time_left - how_long_in_select
        if time_left <= 0:
            return


def send_one_ping(my_socket, dest_addr, id):
    """
    Send one ping to the given >dest_addr<.
    """
    dest_addr  =  socket.gethostbyname(dest_addr)

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    my_checksum = 0

    # Make a dummy heder with a 0 checksum.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, id, 1)
    bytes_in_double = struct.calcsize("d")
    data = (192 - bytes_in_double) * "Q"
    data = struct.pack("d", time.time()) + data

    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(header + data)

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), id, 1
    )
    packet = header + data
    my_socket.sendto(packet, (dest_addr, 1)) # Don't know about the 1


# 2015/11/07  Dayong Wang added one line below
icmp = socket.getprotobyname("icmp")
def do_one(dest_addr, timeout, icmp = 1):
    """
    Returns either the delay (in seconds) or none on timeout.
    """
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error as e:
        if e.errno == 1:
            # Operation not permitted
            e.msg = e.msg + (
                " - Note that ICMP messages can only be sent from processes"
                " running as root."
            )
            raise socket.error(e.msg)
        raise # raise the original error

    my_id = os.getpid() & 0xFFFF

    send_one_ping(my_socket, dest_addr, my_id)
    delay = receive_one_ping(my_socket, my_id, timeout)

    my_socket.close()
    return delay


def verbose_ping(dest_addr, timeout = 2, count = 4):
    """
    Send >count< ping to >dest_addr< with the given >timeout< and display
    the result.
    """
    for i in range(count):
        logging.info("%s: ping %s..." % (i, dest_addr))
        try:
            delay  =  do_one(dest_addr, timeout)
        except socket.gaierror as e:
            logging.error("failed. (socket error: '%s')" % (e[1]))
            break

        if delay  ==  None:
            logging.error("failed. (timeout within %ssec.)" % (timeout))
        else:
            delay  =  delay * 1000
            logging.info("get ping in %0.4fms" % (delay))
    logging.info('')


def w_verbose_ping(dest_addr, count=1, interval=0.2, timeout=1, shell_output=False, silence=False):

    now = time.strftime(TIME_FORMAT, time.localtime(time.time()))
    cmd_out  = ''
    pkt_loss = 0
    pkt_recv = 0
    rtt_min  = 0.0
    rtt_avg  = 0.0
    rtt_max  = 0.0
    rtt_sum  = 0.0
    msg_header = "ping %s:" % (dest_addr)

    for pkt_sent in range(count):
        try:
            delay = do_one(dest_addr, timeout, icmp)
        except socket.gaierror as e:
            logging.error("%s failed (socket error: '%s')" % (msg_header, e[1]))
            return ''
        if delay == None:
            pkt_loss = pkt_loss + 1
            if not silence:
                cmd_out = "%s%s failed (timeout within %s sec)\n" % (cmd_out, msg_header, timeout)
        else:
            pkt_recv = pkt_recv + 1
            delay = delay * 1000
            rtt_sum = rtt_sum + delay
            if rtt_max < delay:
                rtt_max = delay
            if rtt_min > delay or rtt_min == 0:
                rtt_min = delay
            if not silence:
                cmd_out = "%s%s icmp_seq=%d time=%0.4f ms\n" % (cmd_out, msg_header, pkt_sent, delay)
        time.sleep(interval)

    if pkt_recv > 0:
        pkt_sent = pkt_sent + 1
        loss = pkt_loss / pkt_sent
        rtt_avg = rtt_sum / pkt_recv
        cmd_out = """
%s
--- [%s] %s ping statistics ---
%d packets transmitted, %d received, %0.2f%% packet loss, time %0.3fms
rtt min/avg/max/mdev = %0.3f/%0.3f/%0.3f/0.000 ms
""" % ( cmd_out, now, dest_addr, pkt_sent, pkt_recv, loss, rtt_sum, rtt_min, rtt_avg, rtt_max)

        if shell_output:
            return cmd_out
        else:
            return "%s, %s, %s, %s, %0.2f%%, %0.3f, %0.3f, %0.3f" % \
                   (now, dest_addr, pkt_sent, pkt_recv, loss, rtt_min, rtt_avg, rtt_max)

    else:
        return ''



def w_shell_ping(dest_addr, count=1, interval=0.2, timeout=1, shell_output=False, silence=False, bind=''):

    now = time.strftime(TIME_FORMAT, time.localtime(time.time()))
    pkt_loss = ''
    pkt_all  = ''
    pkt_rcv  = ''
    rtt_min  = ''
    rtt_avg  = ''
    rtt_max  = ''

    if bind != '':
        bind = '-I %s' % bind

    ping_cmd = 'ping -c %s -i %s -W %s %s %s' % (count, interval, timeout, bind, dest_addr)
    logging.debug(ping_cmd)

    if platform.system() == 'Darwin':
        ping_cmd = re.sub(" -W [\\d+.]", '', ping_cmd)
    ping_out = sys_cmd(ping_cmd)[0].split("\n")

    if len(ping_out) < 2:
        logging.error("Wrong output of ping")
        return ''

    if shell_output:
        tmp_out = ''
        for str_line in ping_out:
            tmp_out = '%s\n%s' % (tmp_out, str_line)
        return tmp_out

    while len(ping_out) > 0:

        str_line = ping_out[len(ping_out)-1]
        logging.debug(str_line)

        if ( str_line.find('rtt') == 0 or str_line.find('round-trip') == 0) :
            str_line = re.sub(' .*', '', re.sub('^.*= *', '', str_line))
            try:
                rtt_min, rtt_avg, rtt_max, rtt_mdev = str_line.split('/')
            except:
                return ''

        if str_line.find('packet loss') > 0:
            pkt_all  = re.sub(' packets.*$',  '', str_line)
            pkt_rcv  = re.sub(' packets received.*$', '', str_line)
            pkt_rcv  = re.sub('^.*, ', '', pkt_rcv)
            pkt_loss = "%0.2f%%" % (100 * (float(pkt_all) - float(pkt_rcv)) / float(pkt_all))
        if pkt_loss != '' and rtt_avg != '':
            break

        ping_out.pop()

    return "%s, %s, %s, %s, %s, %s, %s, %s" % \
           (now, dest_addr, pkt_all, pkt_rcv, pkt_loss, rtt_min, rtt_avg, rtt_max)


def w_ping(dst_ip, ping_count=1, ping_interval=0.2, ping_timeout=1, ping_bind='', dir=".", silence=False, shell_output=False, pyping=False):

    # dst_ip
    if re.search("^(\d{1,3}\\.){3}\d{1,3}$", dst_ip) == None:
        return False
    # do ping
    if not pyping:
        cmd_out = w_shell_ping(dst_ip, ping_count, ping_interval, ping_timeout, shell_output, silence, ping_bind)
    else:
        cmd_out = w_verbose_ping(dst_ip, ping_count, ping_interval, ping_timeout, shell_output, silence)
    if cmd_out == '':
        return False
    if not shell_output:
        #timestamp, dst_ip, sent, recieved, loss, min, avg, max, bind_addr/int
        cmd_out = "%s, %s" % (cmd_out, ping_bind)
    if not silence:
        logging.info(cmd_out)

    if len(dir) > 0:
        # write to file
        output_file = "%s/%s" % (dir, dst_ip)
        output_path = os.path.dirname(output_file)

        if not os.path.exists(output_path):
            try:
                cmd_mkdir = 'mkdir -p %s' % (output_path)
                sys_cmd(cmd_mkdir)
            except:
                logging.error('mkdir %s failed!' % (output_path))
                return False
        try:
            f_out = open(output_file, 'a')
            f_out.write("%s\n" % (cmd_out))
            f_out.close()
        except:
            logging.error('file %s is failed to write.' % (output_file))
            return False

    return True


def boss(ip_list):
    ip_len = len(ip_list)
    for i in range(0, ip_len):
        tasks.put(ip_list[i].strip())
    logging.debug("Assigned all task.")


def worker(ping_count, ping_interval, ping_timeout, ping_bind, dir, silence, shell_output, pyping):
    try:
        while True:
            ip = tasks.get(timeout=0.001)   # timeout and queue size effects the total execution time
            w_ping(ip, ping_count, ping_interval, ping_timeout, ping_bind, dir, silence, shell_output, pyping)
            gevent.sleep(0)
    except Empty:
        # logging.debug("Queue is empty!")
        pass


if __name__ == '__main__':

    p = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter,
            description='''  This is a pure-python-ping, it was designed for pinging a lot of IP addresses.
  But pure-python-ping gets wrong latency and I can not fix it. So I set Linux
  ping as default, and pure-python-ping can be enabled with --pyping. 
''',
            epilog='''

Log format:

  yyyy-mm-dd HH:MM:SS, ip, pkt_sent, pkt_recv, loss, rtt_min, rtt_avg, rtt_max, bind_addr/interface


Example:

  %s --ip 192.168.0.1,192.168.0.2
  %s -f ip.test -d /tmp/test/ -i 0.1 -t 5
  %s --file ip.test --dir /tmp/test/ --interval 0.1 --timeout 5
  ''' % (sys.argv[0], sys.argv[0], sys.argv[0])
        )

    p.add_argument("-b", "--bind",      type=str,   default="",     help="Source IP address or Interface of Linux ping command.")
    p.add_argument("-c", "--count",     type=int,   default=1,      help="Same to -c of ping, accepts 0 to 1000, default is 1.")
    p.add_argument("-d", "--dir",       type=str,   default="",     help='''Default is blank, it's where the ping result to be stored only when dir is specified.
Example:
/var/log/w-ping/$(date "+%%Y")/$(date "+%%Y%%m%%d")/
''')
    p.add_argument("-i", "--interval",  type=float, default=0.2,    help="Same to -i of ping, accepts 0 to 60, default is 0.2s, less than 0.2 needs root privilege.")
    p.add_argument("--ip",              type=str,                   help="Destination IP list.")
    p.add_argument("-f", "--file",      type=str,                   help="Destination IP list file.")
    p.add_argument("-l", "--log",       type=str,   default="",     help="Log file, default is not set, then log to stdout.")
    p.add_argument("--level",           type=int,   default=20,     help="Log level, could be 50(critical), 40(error), 30(warning), 20(info) and 10(debug), default is 20.")
    p.add_argument("-m", "--max",       type=int,   default=1000,   help="The maximum threads/processes could be spread each time, default is 1000.")
    p.add_argument("--pyping",          action="store_true",        help="Use pure python ping instead of Linux ping, default is Linux ping.")
    p.add_argument("--shell",           action="store_true",        help="Use Linux ping output style instead of csv.")
    p.add_argument("-s", "--silence",   action="store_true",        help="Silence mode.")
    p.add_argument("-t", "--timeout",   type=float, default=1,      help="Timeout of each thread, accepts 0.01 to 60s, default is 1s.")
    args = p.parse_args()

    logging.basicConfig(level=args.level,
        format='%(asctime)s [%(levelname)s] [%(filename)s, line:%(lineno)d] %(message)s',
        datefmt=TIME_FORMAT,
        filename=args.log,
        filemode='w')

    # ip list
    ip_list = list()
    if args.ip:
        if not re.match("[\d,.]+", args.ip):
            logging.warning("%s is not valid ip address." % (args.ip))
            sys.exit()
        ip_list = args.ip.split(',')
    elif args.file:
        if not os.path.exists(args.file):
            logging.warning('%s does not exist, please specified host with --ip or --file.\n' % (args.file))
            sys.exit()
        f_ip = open(args.file)
        ip_list = f_ip.readlines()
        f_ip.close()
    else:
        p.print_help()
        sys.exit()

    # count
    if args.count < 0 or args.count > 1000:
        args.count = 1
 
    # interval
    if args.interval < 0 or args.interval > 60:
        args.interval = 0.2
 
    # timeout
    if args.timeout < 0.01 or args.timeout > 60:
        args.timeout = 1

    # gevent
    try:
        list_gevent = list()
        list_gevent.append(gevent.spawn(boss, ip_list))
        for i in range(0, args.max):
            list_gevent.append(gevent.spawn(worker, args.count, args.interval, args.timeout, args.bind, args.dir, args.silence, args.shell, args.pyping))
        gevent.joinall(list_gevent)
    except:
        print('')

    # exit
    sys.exit()



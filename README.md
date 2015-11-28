# w-ping


Author
==============
Wang Dayong (Email: wandering_997@sina.com, http://weibo.com/wandering997)


Help
==============

[root@TEST w-ping]# ./w-ping.py

Description:

    This is a python pure ping, it was designed for pinging a lot of IP addresses.

Options:

    --count <num>           Same to -c of ping, accepts 0 to 1000, default is 1.

    --datadir <path>        The path to place output files, default is current directory.
                            if given then --silent will be enabled.
                            Example:
                            /var/log/w-ping/$(date "+%Y")/$(date "+%Y%m%d")/

    --interval              Same to -i of ping, accepts 0 to 60, default is 0.01.

    --ip <ip1,ip2,...>      IP list to ping destination.

    --ipfile <file_name>    File of IP list, --ip has higher priority than --ipfile.

    --shellping             Use traditional shell ping output instead of csv output.

    --silent                Silence mode, will be eanbled while --datadir was given.

    --src <string>          Source name of ping, is hostname mostly, default is n/a.

    --timeout <seconds>     Time to wait for ping executing, default is 1 seconds.

    --thread <num>          The maximum threads could be spread each time, default is 1000.


Log format (csv):

    yyyy-mm-dd HH:MM:SS, ip, pkt_sent, pkt_recv, loss, rtt_min, rtt_avg, rtt_max, src


Example:

    w-ping.py --ip 192.168.0.1
    w-ping.py --ipfile ./ip.test --datadir /tmp/test --interval 0 --timeout 0.1


[root@TEST w-ping]#


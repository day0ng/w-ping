# w-ping

This is a pure python ping, and it's light and simple. The original code of python
ping is from https://github.com/samuel/python-ping/.


Author
==============
Wang Dayong (Email: wandering_997@sina.com, http://weibo.com/wandering997)


Help
==============

[root@TEST w-ping]# ./w-ping.py

Description:

    This is a pure python ping, it was designed for pinging a lot of IP addresses.

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


Examples
==============

These are some examples for different options:

    [root@TEST w-ping]#
    [root@TEST w-ping]# ./w-ping.py --ip 192.168.0.1
    2015-11-28 15:50:42, 192.168.0.1, 1, 1, 0.00%, 3.178, 3.178, 3.178, n/a
    [root@TEST w-ping]#
    [root@TEST w-ping]# ./w-ping.py --ip 192.168.0.1 --count 10
    2015-11-28 15:50:45, 192.168.0.1, 10, 10, 0.00%, 2.667, 5.880, 21.524, n/a
    [root@TEST w-ping]#
    [root@TEST w-ping]#
    [root@TEST w-ping]# ./w-ping.py --ip 192.168.0.1 --shellping

    ping 192.168.0.1: icmp_seq=0 time=2.7039 ms

    --- [2015-11-28 15:50:48] 192.168.0.1 ping statistics ---
    1 packets transmitted, 1 received, 0.00% packet loss, time 2.704ms
    rtt min/avg/max/mdev = 2.704/2.704/2.704/0.000 ms

    [root@TEST w-ping]#
    [root@TEST w-ping]# ./w-ping.py --ip 192.168.0.1 --shellping --count 10

    ping 192.168.0.1: icmp_seq=0 time=3.0239 ms
    ping 192.168.0.1: icmp_seq=1 time=2.6319 ms
    ping 192.168.0.1: icmp_seq=2 time=3.6349 ms
    ping 192.168.0.1: icmp_seq=3 time=2.7049 ms
    ping 192.168.0.1: icmp_seq=4 time=2.8689 ms
    ping 192.168.0.1: icmp_seq=5 time=2.8410 ms
    ping 192.168.0.1: icmp_seq=6 time=2.9349 ms
    ping 192.168.0.1: icmp_seq=7 time=2.7881 ms
    ping 192.168.0.1: icmp_seq=8 time=2.9690 ms
    ping 192.168.0.1: icmp_seq=9 time=2.9330 ms

    --- [2015-11-28 15:51:33] 192.168.0.1 ping statistics ---
    10 packets transmitted, 10 received, 0.00% packet loss, time 29.330ms
    rtt min/avg/max/mdev = 2.632/2.933/3.635/0.000 ms

    [root@TEST w-ping]#
    [root@TEST w-ping]#
    [root@TEST w-ping]# time ./w-ping.py --ip 192.168.0.1 --shellping --count 10 --interval 0.5

    ping 192.168.0.1: icmp_seq=0 time=2.7971 ms
    ping 192.168.0.1: icmp_seq=1 time=2.9240 ms
    ping 192.168.0.1: icmp_seq=2 time=2.7552 ms
    ping 192.168.0.1: icmp_seq=3 time=3.2270 ms
    ping 192.168.0.1: icmp_seq=4 time=2.8849 ms
    ping 192.168.0.1: icmp_seq=5 time=4.6968 ms
    ping 192.168.0.1: icmp_seq=6 time=2.7409 ms
    ping 192.168.0.1: icmp_seq=7 time=3.3519 ms
    ping 192.168.0.1: icmp_seq=8 time=2.7380 ms
    ping 192.168.0.1: icmp_seq=9 time=3.2411 ms

    --- [2015-11-28 16:03:40] 192.168.0.1 ping statistics ---
    10 packets transmitted, 10 received, 0.00% packet loss, time 31.357ms
    rtt min/avg/max/mdev = 2.738/3.136/4.697/0.000 ms


    real	0m5.083s
    user	0m0.037s
    sys	    0m0.012s
    [root@TEST w-ping]#
    [root@TEST w-ping]#
    [root@TEST w-ping]#
    [root@TEST w-ping]#
    [root@TEST w-ping]# ls -lh
    total 148K
    -rw-r--r-- 1 root root 130K Nov 28 14:14 ip
    -rwxr-xr-x 1 root root  15K Nov 28 15:58 w-ping.py
    [root@TEST w-ping]#
    [root@TEST w-ping]# tail ip
    10.168.184.39
    10.168.184.40
    10.168.185.11
    10.168.185.12
    10.168.185.13
    10.168.185.14
    10.168.185.15
    10.168.185.16
    10.168.185.17
    10.168.185.18
    [root@TEST w-ping]#
    [root@TEST w-ping]# cat ip |wc -l
    10000
    [root@TEST w-ping]#
    [root@TEST w-ping]# time ./w-ping.py --ipfile ip --datadir ./test

    real	0m10.995s
    user	0m7.926s
    sys	    0m6.592s
    [root@TEST w-ping]#
    [root@TEST w-ping]#
    [root@TEST w-ping]# ls -lh
    total 424K
    -rw-r--r-- 1 root root 130K Nov 28 14:14 ip
    drwxr-xr-x 2 root root 276K Nov 28 15:59 test
    -rwxr-xr-x 1 root root  15K Nov 28 15:58 w-ping.py
    [root@TEST w-ping]#
    [root@TEST w-ping]#
    [root@TEST w-ping]# ls test/ |wc -l
    9870
    [root@TEST w-ping]#
    [root@TEST w-ping]# ls test/ |sort > fail
    [root@TEST w-ping]#
    [root@TEST w-ping]# diff ip fail |head
    871,1000d870
    < 10.0.2.232
    < 10.0.2.233
    < 10.0.2.234
    < 10.0.2.235
    < 10.0.2.236
    < 10.0.2.237
    < 10.0.2.238
    < 10.0.2.239
    < 10.0.2.24
    [root@TEST w-ping]



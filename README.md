# [w-ping](https://github.com/day0ng/w-ping)

This is a pure python ping, and it's light and simple. The original code of python ping is from [https://github.com/samuel/python-ping/](https://github.com/samuel/python-ping/).



2016-09-15:

There's something wrong with raw-python-ping. It gets wrong latency, and I can not fix it. So I set Linux ping as default instead of pure-python-ping. The pure-python-ping can be enabled with --pythonping.



## [Author](https://github.com/day0ng/w-ping#author)

Wang Dayong (Email: [wandering_997@sina.com](mailto:wandering_997@sina.com), [Weibo: wandering997](http://weibo.com/wandering997))



## [Help](https://github.com/day0ng/w-ping#help)

```bash
[root@TEST w-ping]# ./w-ping.py
usage: w-ping.py [-h] [--bind BIND] [--count COUNT] [--datadir DATADIR]
                 [--interval INTERVAL] [--ip IP] [--ipfile IPFILE] [--log LOG]
                 [--loglevel LOGLEVEL] [--max MAX] [--pythonping]
                 [--shelloutput] [--silence] [--timeout TIMEOUT]

  This is a pure-python-ping, it was designed for pinging a lot of IP addresses.
  But pure-python-ping gets wrong latency and I can not fix it. So I set Linux
  ping as default, and pure-python-ping can be enabled with --pythonping.

optional arguments:
  -h, --help           show this help message and exit
  --bind BIND          Source IP address or Interface of Linux ping command.
  --count COUNT        Same to -c of ping, accepts 0 to 1000, default is 1.
  --datadir DATADIR    Where the ping result to be stored, default is current directory.
                       Example:
                       /var/log/w-ping/$(date "+%Y")/$(date "+%Y%m%d")/
  --interval INTERVAL  Same to -i of ping, accepts 0 to 60, default is 0.2s, less than 0.2 needs root privilege.
  --ip IP              Destination IP list.
  --ipfile IPFILE      Destination IP list file.
  --log LOG            Log file, default is not set, then log to stdout.
  --loglevel LOGLEVEL  Log level, could be 50(critical), 40(error), 30(warning), 20(info) and 10(debug), default is 20.
  --max MAX            The maximum threads/processes could be spread each time, default is 1000.
  --pythonping         Use pure python ping instead of Linux ping, default is Linux ping.
  --shelloutput        Use Linux ping output style instead of csv.
  --silence            Silence mode.
  --timeout TIMEOUT    Timeout of each thread, accepts 1 to 60, default is 1s.

Log format:

  yyyy-mm-dd HH:MM:SS, ip, pkt_sent, pkt_recv, loss, rtt_min, rtt_avg, rtt_max, bind_addr/interface

Example:

  /nms/bin/w-ping.py --ip 192.168.0.1,192.168.0.2
  /nms/bin/w-ping.py --ipfile ip.test --datadir /tmp/test/ --interval 0.1 --timeout 5

[root@TEST w-ping]#
```



## [Examples](https://github.com/day0ng/w-ping#examples)

These are some examples for different options:

```shell
[root@TEST w-ping]#
[root@TEST w-ping]# ./w-ping.py --ip 192.168.0.1
2015-11-28 15:50:42, 192.168.0.1, 1, 1, 0.00%, 3.178, 3.178, 3.178, 
[root@TEST w-ping]#
[root@TEST w-ping]# ./w-ping.py --ip 192.168.0.1 --count 10
2015-11-28 15:50:45, 192.168.0.1, 10, 10, 0.00%, 2.667, 5.880, 21.524,
[root@TEST w-ping]#
[root@TEST w-ping]#
[root@TEST w-ping]# ./w-ping.py --ip 192.168.0.1 --shellping

ping 192.168.0.1: icmp_seq=0 time=2.7039 ms

--- [2015-11-28 15:50:48] 192.168.0.1 ping statistics ---
1 packets transmitted, 1 received, 0.00% packet loss, time 2.704ms
rtt min/avg/max/mdev = 2.704/2.704/2.704/0.000 ms

[root@TEST w-ping]#
[root@TEST w-ping]# ./w-ping.py --ip 192.168.0.1 --shelloutput --count 10

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
[root@TEST w-ping]# time ./w-ping.py --ip 192.168.0.1 --shelloutput --count 10 --interval 0.5

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


real    0m5.083s
user    0m0.037s
sys     0m0.012s
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

real    0m10.995s
user    0m7.926s
sys     0m6.592s
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
```
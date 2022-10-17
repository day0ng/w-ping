# [w-ping](https://github.com/day0ng/w-ping)

This is a pure python ping, and it's light and simple. The original code of python ping is from [https://github.com/samuel/python-ping/](https://github.com/samuel/python-ping/).



2016-09-15:

There's something wrong with pure-python-ping. It gets wrong latency, and I can not fix it. So I set Linux ping as default instead of pure-python-ping. The pure-python-ping can be enabled with --pythonping.



## [Author](https://github.com/day0ng/w-ping#author)

Wang Dayong (Email: [wandering_997@sina.com](mailto:wandering_997@sina.com), [Weibo: wandering997](http://weibo.com/wandering997))



## [Help](https://github.com/day0ng/w-ping#help)

```bash
[root@TEST w-ping]# ./w-ping.py
usage: w-ping.py [-h] [-b BIND] [-c COUNT] [-d DATADIR] [-i INTERVAL]
                 [--ip IP] [-f IPFILE] [-l LOG] [--loglevel LOGLEVEL] [-m MAX]
                 [--pythonping] [--shelloutput] [-s] [-t TIMEOUT]

  This is a pure-python-ping, it was designed for pinging a lot of IP addresses.
  But pure-python-ping gets wrong latency and I can not fix it. So I set Linux
  ping as default, and pure-python-ping can be enabled with --pythonping.

optional arguments:
  -h, --help            show this help message and exit
  -b BIND, --bind BIND  Source IP address or Interface of Linux ping command.
  -c COUNT, --count COUNT
                        Same to -c of ping, accepts 0 to 1000, default is 1.
  -d DATADIR, --datadir DATADIR
                        Where the ping result to be stored, default is current directory.
                        Example:
                        /var/log/w-ping/$(date "+%Y")/$(date "+%Y%m%d")/
  -i INTERVAL, --interval INTERVAL
                        Same to -i of ping, accepts 0 to 60, default is 0.2s, less than 0.2 needs root privilege.
  --ip IP               Destination IP list.
  -f IPFILE, --ipfile IPFILE
                        Destination IP list file.
  -l LOG, --log LOG     Log file, default is not set, then log to stdout.
  --loglevel LOGLEVEL   Log level, could be 50(critical), 40(error), 30(warning), 20(info) and 10(debug), default is 20.
  -m MAX, --max MAX     The maximum threads/processes could be spread each time, default is 1000.
  --pythonping          Use pure python ping instead of Linux ping, default is Linux ping.
  --shelloutput         Use Linux ping output style instead of csv.
  -s, --silence         Silence mode.
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout of each thread, accepts 0.01 to 60s, default is 1s.

Log format:

  yyyy-mm-dd HH:MM:SS, ip, pkt_sent, pkt_recv, loss, rtt_min, rtt_avg, rtt_max, bind_addr/interface

Example:

  /nms/bin/w-ping.py --ip 192.168.0.1,192.168.0.2
  /nms/bin/w-ping.py -f ip.test -d /tmp/test/ -i 0.1 -t 5
  /nms/bin/w-ping.py --ipfile ip.test --datadir /tmp/test/ --interval 0.1 --timeout 5

[root@TEST w-ping]#
```



## [Examples](https://github.com/day0ng/w-ping#examples)

These are some examples for different options:

```shell
[root@TEST w-ping]#
[root@TEST w-ping]# ./w-ping.py --ip 192.168.0.6
2016-09-16 09:31:09 [INFO] [w-ping.py, line:343] 2016-09-16 09:31:09, 192.168.0.6, 1, 1, 0.00%, 1.749, 1.749, 1.749,
[root@TEST w-ping]#
[root@TEST w-ping]# ./w-ping.py --ip 192.168.0.6 -c 5
2016-09-16 09:32:01 [INFO] [w-ping.py, line:343] 2016-09-16 09:32:00, 192.168.0.6, 5, 5, 0.00%, 1.453, 1.587, 1.822,
[root@TEST w-ping]#
[root@TEST w-ping]# ./w-ping.py --ip 192.168.0.6 --shelloutput
2016-09-16 09:32:31 [INFO] [w-ping.py, line:343]
PING 192.168.0.6 (192.168.0.6) 56(84) bytes of data.
64 bytes from 192.168.0.6: icmp_seq=1 ttl=252 time=1.61 ms

--- 192.168.0.6 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 1ms
rtt min/avg/max/mdev = 1.615/1.615/1.615/0.000 ms

[root@TEST w-ping]#
[root@TEST w-ping]# ./w-ping.py --ip 192.168.0.6 --shelloutput -c 5
2016-09-16 09:33:13 [INFO] [w-ping.py, line:343]
PING 192.168.0.6 (192.168.0.6) 56(84) bytes of data.
64 bytes from 192.168.0.6: icmp_seq=1 ttl=252 time=1.94 ms
64 bytes from 192.168.0.6: icmp_seq=2 ttl=252 time=1.90 ms
64 bytes from 192.168.0.6: icmp_seq=3 ttl=252 time=1.97 ms
64 bytes from 192.168.0.6: icmp_seq=4 ttl=252 time=1.47 ms
64 bytes from 192.168.0.6: icmp_seq=5 ttl=252 time=1.51 ms

--- 192.168.0.6 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 804ms
rtt min/avg/max/mdev = 1.470/1.762/1.972/0.225 ms

[root@TEST w-ping]#
[root@TEST w-ping]# cat ip |wc -l
1000
[root@TEST w-ping]#
[root@TEST w-ping]# tail ip
10.168.212.58
10.168.212.60
10.168.212.70
10.168.212.72
10.168.212.74
10.168.212.76
10.168.212.80
10.168.212.84
10.168.212.85
10.168.212.88
[root@TEST w-ping]#
[root@TEST w-ping]# time ./w-ping.py -f ip -d ./test
real	0m10.226s
user	0m2.464s
sys	    0m4.172s
[root@TEST w-ping]#
[root@TEST w-ping]# ls test/ |wc -l
1000
[root@TEST w-ping]#
[root@TEST w-ping]# [root@CT_YF-NMS-2 140.12]# tail test/10.168.212.88
2016-09-16 22:43:18, 10.168.212.88, 1, 1, 0.00%, 1.214, 1.214, 1.214,
[root@TEST w-ping]#
[root@TEST w-ping]#
```



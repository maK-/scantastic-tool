# scantastic-tool

## It's bloody scantastic

If you like this and are feeling a bit(coin) generous - 1JdSGqg2zGTbpFMJPLbWoXg7Nng3z1Qp58

It works for me: http://makthepla.net/scantastichax.png

 - Dependencies: (DIY - I ain't supportin shit)
 - Masscan - https://github.com/robertdavidgraham/masscan
 - Nmap - https://nmap.org/download.html
 - ElasticSearch - http://www.elasticsearch.org/guide/en/elasticsearch/guide/current/_installing_elasticsearch.html
 - Kibana - http://www.elasticsearch.org/overview/kibana/installation/


This tool can be used to store masscan or nmap data in elasticsearch, 
(the scantastic plugin in the image is not here)

It allows performs distributed directory brute-forcing. 

All your base are belong to us. I might maintain or improve this over time. MIGHT.

## Quickstart

### Example usage

Run and import a scan of home /24 network

```
./scantastic.py -s -H 192.168.1.0/24 -p 80,443 -x homescan.xml (with masscan)
./scantastic.py -ns -H 192.168.1.0/24 -p 80,443 -x homescan.xml (with nmap)
```

Export homescan to a list of urls

```
./scantastic.py -eurl -x homescan.xml > urlist (with masscan)
./scantastic.py -nurl -x homescan.xml > urlist (with nmap)
```

Brute force the url list using wordlist and put results into index homescan
using 10 threads (By default it uses 1 thread)

```
./scantastic.py -d -u urlist -w some_wordlist -i homescan -t 10
```

```
root@ubuntu:~/scantastic-tool# ./scantastic.py -h
usage: scantastic.py [-h] [-v] [-d] [-s] [-noes] [-sl] [-in] [-e] [-eurl]
                     [-del] [-H HOST] [-p PORTS] [-x XML] [-w WORDS] [-u URLS]
                     [-t THREADS] [-esh ESHOST] [-esp PORT] [-i INDEX]
                     [-a AGENT]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Version information
  -d, --dirb            Run directory brute force. Requires --urls & --words
  -s, --scan            Run masscan on single range. Specify --host & --ports
                        & --xml
  -ns, --nmap           Run Nmap on a single range specify -H & -p
  -noes, --noelastics   Run scan without elasticsearch insertion
  -sl, --scanlist       Run masscan on a list of ranges. Requires --host &
                        --ports & --xml
  -nsl, --nmaplist      Run Nmap on a list of ranges -H & -p & -x
  -in, --noinsert       Perform a scan without inserting to elasticsearch
  -e, --export          Export a scan XML into elasticsearch. Requires --xml
  -eurl, --exporturl    Export urls to scan from XML file. Requires --xml
  -nurl, --exportnmap   Export urls from nmap XML, requires -x
  -del, --delete        Specify an index to delete.
  -H HOST, --host HOST  Scan this host or list of hosts
  -p PORTS, --ports PORTS
                        Specify ports in masscan format. (ie.0-1000 or
                        80,443...)
  -x XML, --xml XML     Specify an XML file to store output in
  -w WORDS, --words WORDS
                        Wordlist to be used with --dirb
  -u URLS, --urls URLS  List of Urls to be used with --dirb
  -t THREADS, --threads THREADS
                        Specify the number of threads to use.
  -esh ESHOST, --eshost ESHOST
                        Specify the elasticsearch host
  -esp PORT, --port PORT
                        Specify ElasticSearch port
  -i INDEX, --index INDEX
                        Specify the ElasticSearch index
  -a AGENT, --agent AGENT
                        Specify a User Agent for requests
```

Use -noes and -in scans to not import scans by default upon completion of a scan

# scantastic-tool
It's bloody scantastic
======================

It works for me.
http://makthepla.net/scantastichax.png - Old Example

Dependencies: (DIY - I ain't supportin shit)
Masscan - https://github.com/robertdavidgraham/masscan
ElasticSearch - http://www.elasticsearch.org/guide/en/elasticsearch/guide/current/_installing_elasticsearch.html
Kibana - http://www.elasticsearch.org/overview/kibana/installation/

Python libs -
pip install elasticsearch
pip install requests
pip install netaddr
pip install xmltodict

This tool can be used to store masscan data in elasticsearch, 
(the scantastic plugin in the image is not here)
It allows the output of a directory busting tool to be inserted also. 
All your base are belong to us. I might maintain or improve this over time. MIGHT.

quickstart: - example usage

Run and import a scan of home /24 network
./scantastic.py -s -H 192.168.192.0/24 -p 80,443 -x homescan.xml

Export homescan to a list of urls
./scantastic.py -eurl -x homescan.xml > urlist

Brute force the url list using wordlist and put results into index homescan
using 10 threads (By default it uses 1 thread)
./scantastic.py -d -u urlist -w some_wordlist -i homescan -t 10



root@ubuntu:~/scantastic-tool# ./scantastic.py -h
usage: scantastic.py [-h] [-d] [-s] [-sl] [-e] [-eurl] [-del] [-H HOST]
                     [-p PORTS] [-x XML] [-w WORDS] [-u URLS] [-t THREADS]
                     [-esh ESHOST] [-esp PORT] [-i INDEX] [-a AGENT]

optional arguments:
  -h, --help            show this help message and exit
  -d, --dirb            Run directory brute force. Requires --urls & --words
  -s, --scan            Run masscan on single range. Specify --host & --ports
                        & --xml
  -sl, --scanlist       Run masscan on a list ranges. Requires --host &
                        --ports & --xml
  -e, --export          Export a scan XML into elasticsearch. Requires --xml
  -eurl, --exporturl    Export urls to scan from XML file. Requires --xml
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

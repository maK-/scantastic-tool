# scantastic-tool
It's bloody scantastic
======================

This tool can be used to store masscan data in elasticsearch,
It also allows the output of a directory busting tool to be
inserted also. All your base are belong to us.


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


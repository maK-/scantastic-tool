#!/usr/bin/python
#./showRange.py [127.0.0.0/RANGE]
import sys
from netaddr import *

addr=sys.argv[1]

ip = IPNetwork(addr)
print "from:    ",str(ip.network)
print "to:      ",str(ip.broadcast)


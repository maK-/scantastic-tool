#!/usr/bin/env python
# A class to run masscan and import the results to ES

import subprocess
import socket
import xmltodict
from elasticsearch import Elasticsearch
from datetime import datetime


class Masscan:
    # Initialize with range, output, ports

    def __init__(self, ip_r, xml_o, ps):
        self.ip_range = ip_r
        self.xml_output = xml_o
        self.ports = ps

    def run(self):
        self.args = ("masscan", "-sS", "-Pn", self.ip_range,
                     "-oX", self.xml_output, "--rate=15000", "-p",
                     self.ports, "--open")
        popen = subprocess.Popen(self.args, stdout=subprocess.PIPE)
        popen.wait()
        self.output = popen.stdout.read()
        print "Scan completed!"

    def runfile(self):
        self.args = ("masscan", "-sS", "-Pn", "-iL", self.ip_range,
                     "-oX", self.xml_output, "--rate=15000", "-p", self.ports,
                     "--open")
        popen = subprocess.Popen(self.args, stdout=subprocess.PIPE)
        popen.wait()
        self.output = popen.stdout.read()
        print "Scan completed!"

    def import_es(self, es_index, host, port):
        es = Elasticsearch([{u'host': host, u'port': port}])
        try:
            with open(self.xml_output, "r") as xmlfile:
                data = xmlfile.read().replace('\n', '')
            xml = xmltodict.parse(data)
            nmaprun = xml['nmaprun']
            host = nmaprun['host']
        except:
            print "IO Error"
        for entry in host:
            port = entry['ports']['port']
            try:
                name, alias, addrlist = socket.gethostbyaddr(entry['address']['@addr'])
            except socket.herror:
                name = entry['address']['@addr']
            dataentry = {
                'timestamp': datetime.now(),
                'ip': entry['address']['@addr'],
                'port': port['@portid'],
                'name': name,
                'link': 'http://' + name + '/'
            }
            result = es.index(index=es_index, doc_type='hax', body=dataentry)
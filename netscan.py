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


class Nmap:
    # Initialize with range, output, ports

    def __init__(self, ip_r, xml_o, ps):
        self.ip_range = ip_r
        self.xml_output = xml_o
        self.ports = ps

    def run(self):
        self.args = ("nmap", "-sS", "-Pn", self.ip_range,
                     "-oX", self.xml_output, "-p", self.ports, "--open")
        popen = subprocess.Popen(self.args, stdout=subprocess.PIPE)
        popen.wait()
        self.output = popen.stdout.read()
        print "Scan completed!"

    def runfile(self):
        self.args = ("nmap", "-sS", "-Pn", "-iL", self.ip_range,
                     "-oX", self.xml_output, "-p", self.ports, "--open")
        popen = subprocess.Popen(self.args, stdout=subprocess.PIPE)
        popen.wait()
        self.output = popen.stdout.read()
        print "Scan completed!"

    def toES(address, ports, es_index, host, port):
        es = Elasticsearch([{u'host': host, u'port': port}])
        try:
                name, alias, addrlist = socket.gethostbyaddr(address)

        except socket.herror:
                name = address
        dataentry = {
                'timestamp': datetime.now(),
                'ip': address,
                'port': ports,
                'name': name,
                'link': 'http://' + name + '/'
        }
        print dataentry

    def import_es(self, es_index, host, port):
        try:
            with open(self.xml_output, "r") as xmlfile:
                data = xmlfile.read().replace('\n', '')
            xml = xmltodict.parse(data)
            nmaprun = xml['nmaprun']
            scanhost = nmaprun['host']
            for i in scanhost:
                address = i['address'][0]['@addr']
                port1 = dict(i)
                try: #if one result
                        if int(port1['ports']['port']['@portid']) > 0:
                                port2 = port1['ports']['port']['@portid']
                                toES(address, str(port2), es_index, host, port)
                except: #if multiple
                        port2 = i['ports']['port']#[0]['@portid']
                        for z in port2:
                                x = z['@portid']
                                toES(address, str(x), es_index, host, port)
        except IOError, e:
            print e


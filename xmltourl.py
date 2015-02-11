#!/usr/bin/env python
# Generate URLS from scanfile
# ===============================

import xmltodict


class Xml2urls:
    def __init__(self, xmlfile):
        self.xmlf = xmlfile
        self.data = ''
        try:
            with open('xml/' + self.xmlf) as myf:
                self.data = myf.read().replace('\n', '')
        except IOError:
            print 'File IO Error'
        self.xml = xmltodict.parse(self.data)


    def run(self):
        nmaprun = self.xml['nmaprun']
        host = nmaprun['host']

        for entry in host:
            port = entry['ports']['port']
            if int(port['@portid']) == 80:
                name = entry['address']['@addr']
                print 'http://' + name + '/'
            elif int(port['@portid']) == 443:
                name = entry['address']['@addr']
                print 'https://' + name + '/'
            elif int(port['@portid']) == 21:
                name = entry['address']['@addr']
                print 'ftp://' + name + '/'
            else:
                name = entry['address']['@addr']
                print 'http://' + name + ':' + str(port['@portid']) + '/'


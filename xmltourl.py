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

class Xml2urls2:
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
		scanhost = nmaprun['host']
		for i in scanhost:
			address = i['address'][0]['@addr']
			port1 = dict(i)
			try:
				if int(port1['ports']['port']['@portid']) > 0:
					port2 = port1['ports']['port']['@portid']
					if port2 == '80':
						print 'http://'+address+'/'
					elif port2 == '443':
						print 'https://'+address+'/'
					else:
						print 'http://'+address+':'+port2+'/'
			except:
				port2 = i['ports']['port']
				for z in port2:
					x = z['@portid']
					if x == '80':
						print 'http://'+address+'/'
					elif x == '443':
						print 'https://'+address+'/'
					else:
						print 'http://'+address+':'+x+'/'
				

#!/usr/bin/python
import multiprocessing
import argparse
import sys
import requests
import string
from datetime import datetime
from time import sleep
from elasticsearch import Elasticsearch
from masscan import Masscan
from xmltourl import Xml2urls

requests.packages.urllib3.disable_warnings()

def version_info():
	VERSION_INFO = 'Scantastic v1.0'
	AUTHOR_INFO = 'Author: Ciaran McNally - http://makthepla.net'
	print'  _ _ _..__|_ _. __|_o _'
	print' _>(_(_|| ||_(_|_> |_|(_'
	print'========================='
	print VERSION_INFO
	print AUTHOR_INFO

#Split the list of urls into chunks for threading
def split_urls(u, t):
	print 'Number of URLS: '+str(len(urls))
	print 'Threads: '+str(t)
	print 'URLS in each split: '+str(len(urls)/t)
	print '========================='
	sleep(1)
	for i in xrange(0, len(u), t):
		yield u[i:i+t]

def returnIPaddr(u):
	ip = ""
	if u.startswith('http://'):
		remainhttp = u[7:]
		ip = string.split(remainhttp,'/')[0]
	if u.startswith('https://'):
		remainhttps = u[8:]
		ip = string.split(remainhttps,'/')[0]
	return ip

def returnTitle(content):
	t1=''
	t2=''
	if '<title>' in content:
		t1 = string.split(content, '<title>')[1]
		t2 = string.split(t1, '</title>')[0]
	return t2

#Make requests
def requestor(urls, dirb, host, port, agent, esindex):
	data = {}
	es = Elasticsearch([{u'host': host, u'port': port}])
	user_agent = {'User-agent': agent}
	for url in urls:
		urld = url+dirb
		try:
			r = requests.get(urld, timeout=10, headers=user_agent, verify=False)
			stat = r.status_code
			time = datetime.utcnow()
			cont_len = len(r.content)
			title = returnTitle(r.content)
			if len(r.content) >= 500:
				content = r.content[0:500]
			else:
				content = r.content
			ip = returnIPaddr(url)
			if 'image' in r.headers['content-type']:
				content = 'image'
			if(r.status_code == 200):
				print urld+' - '+ str(r.status_code) +':'+ str(len(r.content))
		except requests.exceptions.Timeout:
			#print urld+' - Timeout'
			stat = -1
		except requests.exceptions.ConnectionError:
			#print url+dirb+' - Connection Error!'
			stat = -2
		except requests.exceptions.TooManyRedirects:
			#print urld+' - Too many redirects!'
			stat = -3
		except:
			stat = 0
		
		if stat > 0:
			data = {
				'timestamp': time,
				'ip': ip,
				'status': stat,
				'content-length': cont_len,
				'content': content,
				'title': title,
				'link': url+dirb,
				'directory': dirb
			}
			try:
				if data['status'] == 200:
					result = es.index(index=esindex, doc_type='hax', body=data)
				else:
					pass
			except:
				data['title'] = 'Unicode Error'
				data['content'] = 'Unicode Error'
				if data['status'] == 200:
					result = es.index(index=esindex, doc_type='hax', body=data)
				else:
					pass

#Run regular masscan on specified range
def scan(host, ports, xml, index, eshost, esport, noin):
	ms = Masscan(host, 'xml/'+xml, ports)
	ms.run()
	if(noin == False):
		ms.import_es(index, eshost, esport)
		print ms.output

#Run masscan on file of ranges
def scanlst(hostfile, ports, xml, index, eshost, esport, noin):
	ms = Masscan(hostfile, 'xml/'+xml, ports)
	ms.runfile()
	if(noin == False):
		ms.import_es(index, eshost, esport)
		print ms.output

def export_xml(xml, index, eshost, esport):
	ms = Masscan('x','xml/'+xml,'y')
	ms.import_es(index, eshost, esport)

def delete_index(dindex, eshost, esport):
	url = 'http://'+eshost+':'+str(esport)+'/'+dindex
	print 'deleting index: '+url
	r = requests.delete(url)
	print r.content

def export_urls(xml):
	x = Xml2urls(xml)
	x.run()

if __name__ == '__main__':
	parse = argparse.ArgumentParser()
	parse.add_argument('-v','--version', action='store_true',default=False,
		help='Version information')
	parse.add_argument('-d','--dirb',action='store_true',default=False,
		help='Run directory brute force. Requires --urls & --words')
	parse.add_argument('-s', '--scan',action='store_true',default=False,
		help='Run masscan on single range. Specify --host & --ports & --xml')
	parse.add_argument('-sl', '--scanlist',action='store_true', default='scanlist',
		help='Run masscan on a list ranges. Requires --host & --ports & --xml')
	parse.add_argument('-in','--noinsert', action='store_true', default=False,
		help='Perform a scan without inserting to elasticsearch')
	parse.add_argument('-e', '--export', action='store_true', default=False,
		help='Export a scan XML into elasticsearch. Requires --xml')
	parse.add_argument('-eurl', '--exporturl', action='store_true', default=False,
		help='Export urls to scan from XML file. Requires --xml')
	parse.add_argument('-del','--delete',action='store_true', default=False,
		help='Specify an index to delete.')
	parse.add_argument('-H','--host',type=str, help='Scan this host or list of hosts')
	parse.add_argument('-p', '--ports', type=str, 
		default='21,22,80,443,8000,8080,8443,2080,2443,9090,6000,8888,50080,50443,5900',
		help='Specify ports in masscan format. (ie.0-1000 or 80,443...)')
	parse.add_argument('-x','--xml', type=str,default='scan.xml',
		help='Specify an XML file to store output in')
	parse.add_argument('-w','--words',type=str,default='words',
		help='Wordlist to be used with --dirb')
	parse.add_argument('-u','--urls',type=str,default='urls',
		help='List of Urls to be used with --dirb')
	parse.add_argument('-t','--threads',type=int,default=1,
		help='Specify the number of threads to use.')
	parse.add_argument('-esh','--eshost',type=str,default=u'127.0.0.1',
		help='Specify the elasticsearch host')
	parse.add_argument('-esp','--port',type=int,default=5900,
		help='Specify ElasticSearch port')
	parse.add_argument('-i','--index',type=str,default='scantastic',
		help='Specify the ElasticSearch index')
	parse.add_argument('-a','--agent',type=str,default='Scantastic O_o',
		help='Specify a User Agent for requests')
	args = parse.parse_args()

	if len(sys.argv) <= 1:
		parse.print_help()
		sys.exit(0)
	
	if (args.version):
		version_info()
		
	if (args.scan) and (args.host != None):
		scan(args.host, args.ports, args.xml, args.index, args.eshost, 
				args.port, args.noinsert)
	
	if (args.scanlist) and (args.host != None):
		scanlst(args.host, args.ports, args.xml, args.index, args.eshost, 
				args.port, args.noinsert)	
	
	if (args.export):
		export_xml(args.xml, args.index, args.eshost, args.port)	
	
	if (args.delete):
		delete_index(args.index, args.eshost, args.port)
	
	if (args.exporturl):
		export_urls(args.xml)
		
	if (args.dirb):
		try:
			with open(args.urls) as f:
				urls = f.read().splitlines()
			with open(args.words) as f:
				words = f.read().splitlines()
		except IOError:
			print 'File not found!'
		threads = []
		splitlist = list(split_urls(urls, args.threads))
		for word in words:
			for i in range(0, len(splitlist)):
				p = multiprocessing.Process(target=requestor, 
					args=(splitlist[i], word, args.eshost, args.port, args.agent, args.index))
				threads.append(p)
				p.start()
			try:
				for p in threads:
					p.join()
			except KeyboardInterrupt:
				print "Killing threads..."
				for p in threads:
					p.terminate()

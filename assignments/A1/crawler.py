from bs4 import BeautifulSoup
import urllib, requests, sys
from urlparse import urlparse
from time import sleep

if len(sys.argv) != 2:
	print 'Usage: python crawler.py [url]'
	sys.exit(1)
starturl = sys.argv[1] #get start url
print "starting crawler with " + starturl
if urlparse(starturl).netloc == '':
	starturl = "http://www.cs.odu.edu/~mln/"
	print "Bad url, crawling www.cs.odu.edu/~mln/"


def crawl(crawled, tocrawl):
	while len(tocrawl) > 0:
		url = tocrawl.pop()
		if url not in crawled:
			print "Crawling " + url
			crawled.add(url)
			try:
				res = urllib.urlopen(url)
				html = res.read()
				soup = BeautifulSoup(html, "lxml")
			except IOError:
				continue
			links = soup.find_all('a')
			for each in links:
				try: #skipping unicode errors
					newlink = str(each.get('href'))
				except:
					continue
				if newlink not in tocrawl:
					if urlparse(newlink).netloc != '' and urlparse(newlink).scheme != '':
						tocrawl.add(newlink)
						print "Adding " + newlink

			sleep(5)

tocrawl = set() #set that holds links not crawled yet
tocrawl.add(starturl)
crawled = set() #set that holds the crawled links
crawl(crawled, tocrawl)

print "Crawled " + str(len(crawled)) + " sites"
from Document import Document
from EmailScraper import EmailScraper
from json import dumps
from queue import Queue
from SpellcheckAPI import SpellcheckAPI
from threading import Thread
from time import sleep
from urllib2 import HTTPError, URLError, urlopen
from urlparse import urlsplit

def fetch_url(url):
	print url
	
	try:
		urlHandler = urlopen(url)
		html = urlHandler.read()

		parts = urlsplit(url)
		url_name = '{0.netloc}'.format(parts)
		print url_name

		file_name = 'samples/output/%s' % url_name
		f = open(file_name, 'w')
		f.write(html)
		f.close()

		return file_name
	
	except (HTTPError, URLError) as e:
		print e

def fetch_url_wrapper(urls_q, content_q):
	while not urls_q.empty():
		url = urls_q.get()
		file_name = fetch_url(url)
		content_q.put(file_name)

def spellcheck(file_name):
	d = Document(file_name)
	s = SpellcheckAPI()
	tmp = d.get_text()
	if tmp:
		print dumps(s.spellcheck(tmp), sort_keys = True, indent = 2, separators=(',', ': '))

def spellcheck_wrapper(content_q):
	while not content_q.empty():
		sleep(0.1)
		file_name = content_q.get()
		if file_name:
			spellcheck(file_name)

urls_data = open('samples/urls.txt')
urls = urls_data.readlines()
urls_q = Queue()
for url in urls:
	urls_q.put(url)

content_q = Queue()

fetch_threads = []
for i in range(10):
	t = Thread(target=fetch_url_wrapper, args=(urls_q, content_q, ))
	fetch_threads.append(t)

spellcheck_threads = []
for i in range(10):
	t = Thread(target=spellcheck_wrapper, args=(content_q, ))
	spellcheck_threads.append(t)

for thread in fetch_threads:
	thread.start()
for thread in fetch_threads:
	thread.join()

for thread in spellcheck_threads:
	thread.start()
for thread in spellcheck_threads:
	thread.join()
import boto3
from Document import Document
from EmailScraper import EmailScraper
import os
from queue import Queue
from SpellcheckAPI import SpellcheckAPI
from threading import Thread
from time import sleep
from urllib2 import HTTPError, URLError, urlopen
from urlparse import urlsplit

# given a url, scrapes the html and writes it to a file
def fetch_url(url):
	print 'fetch_url'
	print url
	
	try:
		urlHandler = urlopen(url)
		html = urlHandler.read()

		parts = urlsplit(url)
		url_name = '{0.netloc}'.format(parts)

		file_name = 'samples/output/html/%s' % url_name
		f = open(file_name, 'w')
		f.write(html)
		f.close()

		return file_name
	
	except (HTTPError, URLError) as e:
		'Exception retrieving content from url %s %s' % (url, e)
		return None

def fetch_url_wrapper(urls_q, spellcheck_q):
	print 'fetch_url_wrapper'
	while True:
		for message in urls_q.receive_messages(QueueUrl=urls_q.url, WaitTimeSeconds=10):
			url = message.body.rstrip('\n')
			print 'Fetching url %s' % url
			file_name = fetch_url(url)
			if file_name:
				spellcheck_q.send_message(MessageBody=file_name)
				print 'URL fetch complete. Sending %s to scrape. Removing from scrape queue.' % url
				message.delete()
			else:
				inaccessible_q = sqs.get_queue_by_name(QueueName='inaccessible_urls')
				response = inaccessible_q.send_message(MessageBody=url)
				if not response.get('Failed'):
					message.delete()
			sleep(0.1)

def spellcheck(file_name):
	print 'spellcheck'
	d = Document(file_name)
	s = SpellcheckAPI()
	tmp = d.get_text()
	if tmp:
		head, tail = os.path.split(file_name)
		out_name = 'samples/output/corrections/%s' % tail
		print(s.spellcheck(tmp))
		f = open(out_name, 'w')
		f.write(s.spellcheck(tmp))
		f.close()

def spellcheck_wrapper(spellcheck_q):
	print 'spellcheck_wrapper'
	while True:
		for message in spellcheck_q.receive_messages(QueueUrl=spellcheck_q.url, WaitTimeSeconds=10):
			file_name = message.body.rstrip('\n')
			print 'Content file_name is %s' % file_name
			if file_name:
				spellcheck(file_name)
				print 'Starting spellcheck for %s. Removing from spellcheck queue.' % file_name
				message.delete()
			sleep(0.1)

# get the service resource
sqs = boto3.resource('sqs')

# get the queue
urls_q = sqs.get_queue_by_name(QueueName='urls_to_scrape')
if not urls_q:
	print 'URL queue not found on SQS.'

# get the list of URLs
urls_data = open('samples/urls.txt')
urls = urls_data.readlines()

# write them to the queue
for url in urls:
	url.rstrip('\n')
	response = urls_q.send_message(MessageBody=url)
	if not response.get('Failed'):
		print 'Enqueued message in urls_q %s' % response

spellcheck_q = sqs.get_queue_by_name(QueueName='filename_to_spellcheck')

fetch_threads = []
for i in range(10):
	t = Thread(target=fetch_url_wrapper, args=(urls_q, spellcheck_q, ))
	fetch_threads.append(t)

print 'Sleeping for 5 seconds.'
sleep(5)
print 'Awake.'

spellcheck_threads = []
for i in range(10):
	t = Thread(target=spellcheck_wrapper, args=(spellcheck_q, ))
	spellcheck_threads.append(t)

for thread in fetch_threads:
 	thread.start()
for thread in spellcheck_threads:
	thread.start()

for thread in fetch_threads:
	thread.join()
for thread in spellcheck_threads:
	thread.join()

# e = EmailScraper('samples/urls.txt')
# e.scrape_whois()
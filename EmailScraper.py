from bs4 import BeautifulSoup
from queue import Queue
import re
from requests import *
from threading import Thread
import time
from urlparse import urlsplit
import whois


class EmailScraper:
	
	def __init__(self, file):
		self.file = file

	def scrape_websites(self):
		if not self.file:
			print 'no input file. set input file'
			return

		urls_file = open(self.file)
		urls = Queue()

		for url in urls_file.readlines():
			urls.append(url)

		# set of crawled urls
		processed_urls = set()

		# email result set
		emails = set()

		# iterate through urls
		while len(urls):
			# 
			url = urls.popleft()
			processed_urls.add(url)

			# get base url and path to resolve relative links
			parts = urlsplit(url)
			base_url = '{0.scheme}://{0.netloc}'.format(parts)
			path = url[:url.rfind('/')+1] if '/' in parts.path else url

			# get url content
			try:
				response = requests.get(url)
			except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
				# ignore pages with errors
				continue

			# regexp for emails
			new_emails = set(re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', response.text, re.I))
			emails.update(new_emails)

		print emails
		return emails

	def fetch_whois(self, url):
		print url

		parts = urlsplit(url)
		base_url = '{0.netloc}'.format(parts)

		# strip off www.
		if base_url.startswith('www.'):
			base_url = base_url[4:]

		# get whois content
		w = whois.whois(base_url)

		if w.emails:
			print w.emails

		return w.emails

	def fetch_whois_wrapper(self, urls_q):
		
		url_emails = {}

		while not urls_q.empty():
			url = urls_q.get()
			emails = self.fetch_whois(url)
			time.sleep(0.05)

			if emails:
				if url in url_emails:
					url_emails[url].append(emails)

				else:
					url_emails[url] = emails

		print url_emails

	def scrape_whois(self):
		if not self.file:
			print 'no input file. set input file'
			return

		urls_data = open('samples/urls.txt')
		urls = urls_data.readlines()
		urls_q = Queue()
		for url in urls:
			urls_q.put(url)

		whois_threads = []
		for i in range(10):
			t = Thread(target=self.fetch_whois_wrapper, args=(urls_q, ))
			whois_threads.append(t)

		for thread in whois_threads:
			thread.start()
		for thread in whois_threads:
			thread.join()


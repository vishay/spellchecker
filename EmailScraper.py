from bs4 import BeautifulSoup
from collections import deque
import re
import requests
import requests.exceptions
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
		urls = deque()

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

	def scrape_whois(self):
		if not self.file:
			print 'no input file. set input file'
			return

		urls_file = open(self.file)
		urls = deque()

		for url in urls_file.readlines():
			urls.append(url)

		# set of crawled urls
		processed_urls = set()

		# email result set
		emails = {}

		# iterate through urls
		while len(urls):
			url = urls.popleft()
			processed_urls.add(url)

			# get base url and path to resolve relative links
			parts = urlsplit(url)
			base_url = '{0.netloc}'.format(parts)
			
			# strip off www.
			if base_url.startswith('www.'):
				base_url = base_url[4:]

			# get whois content
			w = whois.whois(base_url)


			if w.emails:
				emails[base_url] = w.emails

			# delay to prevent whois ratelimiting
			time.sleep(0.05)

		return emails


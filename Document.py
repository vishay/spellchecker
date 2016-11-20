from bs4 import BeautifulSoup
import re

class Document:
	
	def __init__(self, filename):
		self.soup = BeautifulSoup(open(filename), 'html.parser')

		# clean the doc 
		for script in self.soup(['script', 'style']):
		   script.replaceWith(' ')    # rip it out

		# get all the text from the document
		# self.text = self.soup.get_text()
		self.text = ' '.join(self.soup.strings)
		self.text = re.sub('\n',' ', self.text)
		self.text = re.sub(' +',' ', self.text)

		self.elements = self.text.split()

		# create dictionary of words, numbers, symbols
		self.words = {}
		self.numbers = {}
		self.symbols = {}

		for elem in self.elements:
			if elem.isdigit():
				if elem in self.numbers:
					self.numbers[elem] = self.numbers[elem] + 1
				else:
					self.numbers[elem] = 1

			elif elem.isalpha():
				if elem in self.words:
					self.words[elem] = self.words[elem] + 1
				else:
					self.words[elem] = 1

			else:
				if elem in self.symbols:
					self.symbols[elem] = self.symbols[elem] + 1
				else:
					self.symbols[elem] = 1

	def get_all_words(self):
		return self.words

	def get_all_numbers(self):
		return self.numbers

	def get_all_symbols(self):
		return self.symbols

	def get_text(self):
		return self.text

	def pretty_print(self, obj):
		import pprint
		pp = pprint.PrettyPrinter(indent = 4)
		return pp.pprint(obj)
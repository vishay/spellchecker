from Document import Document
from EmailScraper import EmailScraper
from SpellcheckAPI import SpellcheckAPI

d = Document('samples/cnn.html')
s = SpellcheckAPI()
print s.spellcheck(d.get_text())

e = EmailScraper('samples/urls.txt')
print e.scrape_whois()
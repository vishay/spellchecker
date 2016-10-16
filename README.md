# spellchecker
Automatic spellchecker for the web

# How to use
from Document import Document
d = Document("samples/nytimes.html")
t = d.get_text()

from SpellCheckAPI import SpellCheckAPI
s = SpellCheckAPI()
s.spellcheck(t)

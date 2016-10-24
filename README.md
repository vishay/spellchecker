# spellchecker
Automatic spellchecker for the web

# How to use
```
from Document import Document
d = Document("samples/nytimes.html")
t = d.get_text()

from SpellCheckAPI import SpellCheckAPI
s = SpellCheckAPI()
s.spellcheck(t)
```
# Todos
1. fetch html content from web, rather than static local file
2. spellchecker should return context (+/- 10 words around typo)
3. parallelize whois requests
4. keep track of emails AND domains, not just emails
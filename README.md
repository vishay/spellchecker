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
1. Bing API fails because request is too long -- fix this
2. fetch html content from web, rather than static local file
3. spellchecker should return context (+/- 10 words around typo)

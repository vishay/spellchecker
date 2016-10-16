from Document import Document
from SpellCheckAPI import SpellCheckAPI

d = Document("samples/cnn.html")
s = SpellCheckAPI()
print s.spellcheck(d.get_text())
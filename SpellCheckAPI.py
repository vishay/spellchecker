
class SpellCheckAPI:
	
	def __init__(self):
		self.API = 'api.cognitive.microsoft.com'

		self.AUTH_KEY = '95da5684bc6645a389bc35ba71732796'
		self.headers = { 'Ocp-Apim-Subscription-Key': self.AUTH_KEY }
	
	def spellcheck(self, text):
		import ast, base64, httplib, urllib

		# needed or else the string is too long, and the request 414s
		t = text[1350:1500]

		self.params = urllib.urlencode({'text': t, 'mode' : 'proof'})

		self.response_dict = {}
		try:
			conn = httplib.HTTPSConnection(self.API)
			conn.request('POST', '/bing/v5.0/spellcheck/?%s' % self.params, '{body}', self.headers)

			response = conn.getresponse()
			response_str = response.read()

			self.response_dict = ast.literal_eval(response_str)

			conn.close()

		except Exception as e:
			print('[Errno {0}] {1}'.format(e.errno, e.strerror))

		return self.response_dict

	def get_replacements_list(self): 

		flagged_tokens = self.response_dict["flaggedTokens"]

		l = []

		for flagged_token in flagged_tokens: 

			offset = flagged_token["offset"]
			token = flagged_token["token"]
			suggestions = flagged_token["suggestions"]

			s = suggestions[0]
			suggestion = s["suggestion"]
			score = s["score"]

			r = {"old": token, "new": suggestion, "offset": offset}

			l.append(r)

		return l
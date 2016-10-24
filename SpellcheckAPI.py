class SpellcheckAPI:
	
	def __init__(self):
		self.API = 'api.cognitive.microsoft.com'

		self.AUTH_KEY = '95da5684bc6645a389bc35ba71732796'
		self.headers = { 'Ocp-Apim-Subscription-Key': self.AUTH_KEY }
	
	def spellcheck(self, text):
		import ast, base64, httplib, urllib

		# iterate through the string, in blocks of max_length characters

		# split the text up by spaces, to make sure we aren't splitting words
		list_text = text.split(" ")

		l = len(list_text)
		max_length = 100
		iterations = l / max_length + 1
		iteration = 0

		self.suggestions = []
		while iteration < iterations:
			first = iteration * max_length
			last = (iteration + 1) * max_length
			iteration = iteration + 1
			buff = list_text[first:last]
			t = " ".join(buff)
	
			# format the request
			params = urllib.urlencode({'text': t.encode('utf-8'), 'mode' : 'proof'})
			try:
				conn = httplib.HTTPSConnection(self.API)
				conn.request('POST', '/bing/v5.0/spellcheck/?%s' % params, '{body}', self.headers)

				response = conn.getresponse()
				response_str = response.read()

				response_dict = ast.literal_eval(response_str)
				conn.close()

				if response_dict['flaggedTokens'] and response_dict['flaggedTokens']:
					self.suggestions.append(response_dict)

			except Exception as e:
				print('[Errno {0}] {1}'.format(e.errno, e.strerror))

		return self.suggestions

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
class CleanString:
	
	def __init__(self, _string):
		self._chars = list(str(_string))
		self._string = _string
	
	# prints a string of characters
	def print_string(self):
		print(self._chars)
		
	# function removes a token from the string of characters
	
	def remove_token(self, token):
		for char in range(0, len(self._string)):
			if self._chars[char] == token:
				self._chars[char] = ''
		self._string = ''.join(self._chars)
		
		return self._string

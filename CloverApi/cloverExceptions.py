import six


class cloverException(Exception):

	def __init__(self, reason, response=None):
		self.reason = six.text_type(reason)
		self.response = response
		Exception.__init__(self, reason)

	def __str__(self):
		return self.reason

class cloverAuthenticationError(cloverException):
	#Clover Authentication Error has the exact same properties
	#as clover Exception for backwards compatibility reasons
	pass




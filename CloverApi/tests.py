import unittest
from api import cloverApi




class CloverTest(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		self.api = cloverApi()

		return super(CloverTest, self).__init__(*args, **kwargs)

	def assertAuthWorks(self):
		if self.api.auth:
			return True

	def assertMerchantFunctionWorks(self):
		if self.api.merchant:
			return True

	def viewMerchantFunctionRespone(self):
		return self.api.merchant(merchant_id="0893Z9PWMPYFR")

	def runTest(self):
		print self.assertAuthWorks()
		print self.assertMerchantFunctionWorks()
		print self.viewMerchantFunctionRespone()


c = CloverTest()
c.runTest()

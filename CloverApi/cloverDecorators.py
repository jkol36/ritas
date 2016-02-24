from cloverExceptions import cloverException



def auth_id_required(func):
	def auth_id_wrapper_function(self, *args, **kwargs):
		try:
			auth_id = kwargs.pop("auth_id")
		except:
			raise cloverException("a auth_id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return auth_id_wrapper_function

def auth_token_required(func):
	def auth_token_wrapper_function(self, *args, **kwargs):
		try:
			self.auth_token
		except:
			raise cloverException("a auth_token is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return auth_token_wrapper_function

def attribute_id_required(func):
	def attribute_id_wrapper_function(self, *args, **kwargs):
		try:
			attribute_id = kwargs.pop("attribute_id")
		except KeyError, e:
			raise cloverException("a attribute_id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return attribute_id_wrapper_function

def category_id_required(func):
	def category_id_wrapper_function(self, *args, **kwargs):
		try:
			category_id = kwargs.pop("category_id")
		except KeyError, e:
			raise cloverException("a category_id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return category_id_wrapper_function

def customer_id_required(func):
	def customer_id_wrapper_function(self, *args, **kwargs):
		try:
			customer_id = kwargs.pop("customer_id")
		except KeyError, e:
			raise cloverException("a customer_id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return customer_id_wrapper_function


def credit_id_required(func):
	def credit_id_wrapper_function(self, *args, **kwargs):
		try:
			credit_id = kwargs.pop("credit_id")
		except KeyError:
			raise cloverException("a credit id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return credit_id_wrapper_function

def developer_id_required(func):
	def developer_id_wrapper_function(self, *args, **kwargs):
		try:
			developer_id = kwargs.pop("developer_id")
		except KeyError:
			raise cloverException("a developer id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return developer_id_wrapper_function

def discount_id_required(func):
	def discount_id_wrapper_function(self, *args, **kwargs):
		try:
			discount_id = kwargs.pop("discount_id")
		except KeyError:
			raise cloverException("a discount id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return discount_id_wrapper_function

def device_id_required(func):
	def device_id_wrapper_function(self, *args, **kwargs):
		try:
			device_id = kwargs.pop("device_id")
		except KeyError:
			raise cloverException("a device id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return device_id_wrapper_function


def employee_id_required(func):
	def employee_id_wrapper_function(self, *args, **kwargs):
		try:
			employee_id = kwargs.pop("employee_id")
		except KeyError:
			raise cloverException("a credit id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return employee_id_wrapper_function

def item_id_required(func):
	def item_id_wrapper_function(self, *args, **kwargs):
		try:
			item_id = kwargs.pop("item_id")
		except KeyError:
			raise cloverException("a item id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return item_id_wrapper_function

def item_group_id_required(func):
	def item_group_id_wrapper_function(self, *args, **kwargs):
		try:
			item_group_id = kwargs.pop("item_group_id")
		except KeyError:
			raise cloverException("a item group id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return item_group_id_wrapper_function



def line_item_id_required(func):
	def line_item_wrapper_function(self, *args, **kwargs):
		try:
			line_item_id = kwargs.pop("line_item_id")
		except KeyError:
			raise cloverException("a line item id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return line_item_wrapper_function

def merchant_id_required(func):
	def merchant_wrapper_function(self, merchant_id, *args, **kwargs):
		if not merchant_id:
			raise cloverException("a merchant id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, merchant_id, *args, **kwargs)
	return merchant_wrapper_function

def modifier_id_required(func):
	def modifier_wrapper_function(self, *args, **kwargs):
		try:
			mod_id = kwargs.pop("mod_id")
		except KeyError:
			raise cloverException("a modifier id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return modifier_wrapper_function

def modifier_group_id_required(func):
	def modifier_group_wrapper_function(self, *args, **kwargs):
		try:
			mod_group_id = kwargs.pop("mod_group_id")
		except KeyError:
			raise cloverException("a mod group id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return modifier_group_wrapper_function

def option_id_required(func):
	def option_id_wrapper_function(self, *args, **kwargs):
		try:
			option_id = kwargs.pop("option_id")
		except KeyError:
			raise cloverException("a option id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return option_id_wrapper_function

def order_type_id_required(func):
	def order_type_id_wrapper_function(self, *args, **kwargs):
		try:
			order_type_id = kwargs.pop("order_type_id")
		except KeyError:
			raise cloverException("a order_type_id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return order_type_id_wrapper_function

def order_id_required(func):
	def order_id_wrapper_function(self, *args, **kwargs):
		try:
			order_id = kwargs.pop("order_id")
		except KeyError:
			raise cloverException("a order id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return order_id_wrapper_function


def pay_id_required(func):
	def pay_id_wrapper_function(self, *args, **kwargs):
		try:
			pay_id = kwargs.pop("pay_id")
		except KeyError:
			raise cloverException("a pay id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return pay_id_wrapper_function

def refund_id_required(func):
	def refund_id_wrapper_function(self, *args, **kwargs):
		try:
			refund_id = kwargs.pop("refund_id")
		except KeyError:
			raise cloverException("a refund id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return refund_id_wrapper_function

def role_id_required(func):
	def role_id_wrapper_function(self, *args, **kwargs):
		try:
			role_id = kwargs.pop("role_id")
		except KeyError:
			raise cloverException("a role id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return role_id_wrapper_function


def shift_id_required(func):
	def shift_id_wrapper_function(self, *args, **kwargs):
		try:
			shift_id = kwargs.pop("shift_id")
		except KeyError:
			raise cloverException("a shift id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return shift_id_wrapper_function




def tax_id_required(func):
	def tax_id_wrapper_function(self, *args, **kwargs):
		try:
			tax_id = kwargs.pop("tax_id")
		except KeyError:
			raise cloverException("a tax id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return tax_id_wrapper_function


def tip_id_required(func):
	def tip_id_wrapper_function(self, *args, **kwargs):
		try:
			tip_id = kwargs.pop("tip_id")
		except KeyError:
			raise cloverException("a tip id is required to call this function. See https://www.clover.com/api_docs for help ")
	return tip_id_wrapper_function
def tag_id_required(func):
	def tag_id_wrapper_function(self, *args, **kwargs):
		try:
			tag_id = kwargs.pop("tag_id")
		except KeyError:
			raise cloverException("a tag id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return tag_id_wrapper_function

def tender_id_required(func):
	def tender_id_wrapper_function(self, *args, **kwargs):
		try:
			tender_id = kwargs.pop("tender_id")
		except KeyError:
			raise cloverException("a tender_id is required to call this function. See https://www.clover.com/api_docs for help.")
		else:
			return func(self, *args, **kwargs)
	return tender_id_wrapper_function





















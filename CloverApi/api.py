import os
import constants

from cached_property import cached_property

from cloverExceptions import (
	cloverException, 
	cloverAuthenticationError,
)

from cloverDecorators import (
	auth_id_required,
	auth_token_required,
	attribute_id_required,
	category_id_required,
	credit_id_required,
	customer_id_required,
	developer_id_required,
	device_id_required,
	discount_id_required,
	employee_id_required,
	item_id_required,
	item_group_id_required,
	line_item_id_required,
	merchant_id_required,
	modifier_id_required,
	modifier_group_id_required,
	option_id_required,
	order_type_id_required,
	order_id_required,
	pay_id_required,
	refund_id_required,
	role_id_required,
	shift_id_required,
	tax_id_required,
	tip_id_required,
	tag_id_required,
	tender_id_required
)

from bind_api import bind_api






class cloverApi(object):

	def __init__(self, merchant_id=None):
		self.merchant_id = merchant_id

	def __enter__(self):
		""" authenticate ourselves and return the cloverApi instance"""
		if self.auth:
			return self
		raise cloverAuthenticationError("could not authenticate")

	def __exit__(self, *args, **kwargs):
		pass

	@property
	def auth(self):
		try:
			self.auth_token = constants.auth_token; #"f4551875dcfbae15de157fb6b55bb685"; #os.environ["authorization_token"]
		except KeyError:
			raise cloverAuthenticationError("could not find your clover api key. Did you add it to your os.environ?")
		return self.auth_token

	@merchant_id_required
	@auth_token_required
	#returns a single merchant based on the merchant id
	def merchant(self, merchant_id=None, action=None):
		print "merchant called"
		print merchant_id
		return bind_api(self, merchant_id=merchant_id, action="merchant")


	@merchant_id_required
	@auth_token_required
	#updates a merchant's fields
	#fields should be a json object. See https://www.clover.com/api_docs#!/merchants/UpdateMerchant
	def update_merchant(self, merchant_id=None, fields=None):
		return bind_api(self, action="update_merchant", merchant_id=merchant_id, fields=fields)

	@merchant_id_required
	@auth_token_required
	#returns a merchants address
	def merchant_address(self, merchant_id=None):
		return bind_api(self, action="merchant_address", merchant_id=merchant_id)

	@merchant_id_required
	@auth_token_required
	#gets a merchant properties
	def merchant_properties(self, merchant_id=None):
		return bind_api(self, action="merchant_properties", merchant_id=merchant_id)

	@merchant_id_required
	@auth_token_required
	#updates a merchants properties
	#body should be a json object. See https://www.clover.com/api_docs#!/merchants/UpdateMerchantProperties
	def update_merchant_properties(self, merchant_id=None, body=None):
		return bind_api(self, action="update_merchant_properties", 
			merchant_id=merchant_id, body=body)

	@merchant_id_required
	@auth_token_required
	#returns a merchants plan
	#body should be a json object. See https://www.clover.com/api_docs#!/merchants/UpdateMerchantProperties
	def merchant_plan(self, merchant_id=None, body=None):
		return bind_api(self, action="merchant_plan", merchant_id=merchant_id, body=body)

	@merchant_id_required
	@auth_token_required
	#returns a default service charge for a merchant
	def default_service_charge(self, merchant_id=None):
		return bind_api(self, action="merchant_default_service_charge", merchant_id=merchant_id)

	@merchant_id_required
	@auth_token_required
	#returns all tip suggestions for a merchant
	#filter_by is optional, but if used should be past as a dictionary with keys being
	#id, name, percentage, enabled, 
	def merchant_tip_suggestions(self, merchant_id=None, filter_by=None):
		return bind_api(self, action="merchant_tip_suggestions", merchant_id=merchant_id, filter_by=filter_by)

	@merchant_id_required
	#returns a single tip_suggestion based on the tip_id
	@tip_id_required
	@auth_token_required
	def merchant_tip_suggestion(self, merchant_id=None, tip_id=None):
		return bind_api(self, action="merchant_tip_suggestion", merchant_id=merchant_id, tip_id=tip_id)

	@merchant_id_required
	@tip_id_required
	@auth_token_required
	#returns an updated merchant tip
	#body should be a json object. See https://www.clover.com/api_docs#!/merchants/UpdateTipSuggestion
	def update_merchant_tip_suggestion(self, merchant_id=None, tip_id=None, body=None):
		return bind_api(self, action="update_merchant_tip_suggestion", merchant_id=merchant_id, tip_id=tip_id, body=body)


	@merchant_id_required
	@auth_token_required
	#returns all merchant order types. Filter fields should be a dictionary. Same with expand_fields.
	#see https://www.clover.com/api_docs#!/merchants/GetOrderTypes
	def all_merchant_order_types(self, merchant_id=None, filter_by=None, expand_fields=None):
		return bind_api(self, action="all_merchant_order_types", merchant_id=merchant_id, filter_by=filter_by, expand_fields=expand_fields)

	@merchant_id_required
	#creates a merchant order type
	#see https://www.clover.com/api_docs#!/merchants/CreateOrderType

	def create_merchant_order_types(self, merchant_id=None, expand_fields=None):
		return bind_api(self, action="create_merchant_order_types", merchant_id=merchant_id, expand_fields=expand_fields)

	@merchant_id_required
	@order_type_id_required
	@auth_token_required
	def merchant_order_type(self, merchant_id=None, order_type_id=None, expand_fields=None):
		return bind_api(self, action="get_merchant_order_type", merchant_id=merchant_id, order_type_id=order_type_id, expand_fields=expand_fields)

	@merchant_id_required
	def update_merchant_order_type(self, merchant_id=None, order_type_id=None):
		return bind_api(self, action="update_metchant_order_type", merchant_id=merchant_id, order_type_id=order_type_id)

	@merchant_id_required
	@auth_token_required
	#returns all merchant roles
	def roles(self, merchant_id=None):
		return bind_api(self, action="merchant_roles", merchant_id=merchant_id)

	@merchant_id_required
	@role_id_required
	@auth_token_required
	def role(self, merchant_id=None, role_id=None):
		return bind_api(self, action="get_role_for_merchant", role_id=role_id)

	@merchant_id_required
	@role_id_required
	@auth_token_required
	def update_role_for_merchant(self, merchant_id=None, role_id=None, body=None):
		return bind_api(self, action="update_role_for_merchant", merchant_id=merchant_id, role_id=role_id, body=body)

	@merchant_id_required
	@role_id_required
	@auth_token_required
	def delete_role_for_merchant(self, merchant_id=None, role_id=None):
		return bind_api(self, action="delete_role_for_merchant", merchant_id=merchant_id, role_id=role_id)


	@merchant_id_required
	@auth_token_required
	def merchant_tenders(self, merchant_id=None, filter_by=None):
		return bind_api(self, action="merchant_tenders", merchant_id=merchant_id, filter_by=filter_by)

	@merchant_id_required
	@tender_id_required
	@auth_token_required
	def merchant_tender(self, merchant_id=None, tender_id=None):
		return bind_api(self, action="merchant_tender", merchant_id=merchant_id, tender_id=tender_id)

	@merchant_id_required
	@auth_token_required
	def merchant_opening_hours(self, merchant_id=None):
		return bind_api(self, action="merchant_opening_hours", merchant_id=merchant_id,)

	@merchant_id_required
	@auth_token_required
	def cash_events(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_cash_events", merchant_id=merchant_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@employee_id_required
	@auth_token_required
	#returns all cash events for a single employee
	def employee_cash_events(self, merchant_id=None, employee_id=None, filter_by=None):
		return bind_api(self, action="mechant_employee_cash_events", merchant_id=merchant_id, employee_id=employee_id, filter_by=filter_by, expand=expand)


	@merchant_id_required
	@device_id_required
	@auth_token_required
	#returns all cash events for a single device id
	def device_cash_events(self, merchant_id=None, device_id=None, filter_by=None):
		return bind_api(self, action="merchants_devices_cash_events", merchant_id=merchant_id, device_id=device_id, filter_by=filter_by, expand=expand)


	@merchant_id_required
	@auth_token_required
	#returns a list of customers for a merchant as a csv
	def merchant_customers_as_csv(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_customers_as_csv", merchant_id=merchant_id, expand=expand)

	@merchant_id_required
	@auth_token_required
	#returns a list of customers for a merchant
	def merchant_customers(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_customers", merchant_id=merchant_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@customer_id_required
	@auth_token_required
	#returns a single customer based on the customer id
	def merchant_customer(self, merchant_id=None, customer_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_customer", customer_id=customer_id, filter_by=filter_by, expand=expand)


	@merchant_id_required
	@auth_token_required
	#returns all employees
	def merchant_employees(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_employees", merchant_id=merchant_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@employee_id_required
	@auth_token_required
	#returns a single employee based on the employee id

	def merchant_employee(self, merchant_id=None, employee_id=None, expand=None):
		return bind_api(self, action="merchant_employee", merchant_id=merchant_id, employee_id=employee_id, expand=expand)


	@merchant_id_required
	@auth_token_required
	def merchant_shifts(self, merchant_id=None, filter_by=None):
		return bind_api(self, action="merchant_shifts", merchant_id=merchant_id, filter_by=filter_by)

	@merchant_id_required
	@shift_id_required
	@auth_token_required
	def merchant_shift(self, merchant_id=None, shift_id=None, expand=None):
		return bind_api(self, merchant_id=merchant_id, shift_id=shift_id, expand=expand)

	@merchant_id_required
	@auth_token_required
	def merchant_shifts_as_csv(self, merchant_id=None, filter_by=None):
		return bind_api(self, action="merchant_shifts_as_csv", merchant_id=merchant_id, filter_by=filter_by)

	@merchant_id_required
	@employee_id_required
	@auth_token_required
	def merchant_employee_shifts(self, merchant_id=None, employee_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_employee_shifts", merchant_id=merchant_id, employee_id=employee_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@employee_id_required
	@shift_id_required
	@auth_token_required
	#returns a single shift for an employee based on the shift id
	def merchant_employee_shift(self, merchant_id=None, employee_id=None, shift_id=None, expand=None):
		return bind_api(self, action="merchant_employee_shift", merchant_id=merchant_id, employee_id=employee_id, shift_id=shift_id, expand=expand)

	@merchant_id_required
	@employee_id_required
	@auth_token_required
	#returns merchange employee orders
	def merchant_employee_orders(self, merchant_id=None, employee_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_employee_orders", merchant_id=merchant_id, employee_id=employee_id, filter_by=filter_by, expand=expand)


	@merchant_id_required
	@auth_token_required
	def merchant_items(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_inventory_items", filter_by=filter_by, expand=expand)

	@merchant_id_required
	@item_id_required
	@auth_token_required
	def merchant_item(self, merchant_id=None, item_id=None, expand=None):
		return bind_api(self, action="merchant_inventory_item", expand=expand)

	@merchant_id_required
	@auth_token_required
	#get the stocks of all merchant inventory items
	def merchant_item_stocks(self, merchant_id=None):
		return bind_api(self, action="merchant_item_stocks", merchant_id=merchant_id)

	@merchant_id_required
	@item_id_required
	@auth_token_required
	#returns the stock of the inventory item
	def merchant_item_stock(self, merchant_id=None, item_id=None):
		return bind_api(self, action="merchant_item_stock", merchant_id=merchant_id, item_id=item_id)

	@merchant_id_required
	@auth_token_required
	#gets all item groups
	def merchant_item_groups(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_item_groups", merchant_id=merchant_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@item_group_id_required
	@auth_token_required
	#returns a single item group based on the id
	def merchant_item_group(self, merchant_id=None, item_group_id=None, expand=None):
		return bind_api(self, action="merchant_item_group", merchant_id=merchant_id, item_group_id=item_group_id, expand=expand)

	@merchant_id_required
	@auth_token_required
	def merchant_tags(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_tags", merchant_id=merchant_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@tag_id_required
	@auth_token_required
	#returns a single tag based on the tag id
	def merchant_tag(self, merchant_id=None, tag_id=None, expand=None):
		return bind_api(self, action="merchant_tag", merchant_id=merchant_id, item_group_id=item_group_id, expand=expand)

	@merchant_id_required
	@item_id_required
	@auth_token_required
	#returns all tags for a specific item
	def merchant_item_tags(self, merchant_id=None, item_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_tag", merchant_id=merchant_id, item_id=item_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@tag_id_required
	@auth_token_required
	#get all items for a specifc tag
	def merchant_items_for_tag(self, merchant_id=None, tag_id=None, filter_by=None):
		return bind_api(self, action="merchant_items_for_tag", merchant_id=None, tag_id=None, filter_by=filter_by)

	@merchant_id_required
	@auth_token_required
	#returns all tax rates
	def merchant_tax_rates(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_tax_rates", merchant_id=merchant_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@tax_id_required
	@auth_token_required
	#returns a single tax rate based on the tax id
	def merchant_tax_rate(self, merchant_id=None, tax_id=None, expand=None):
		return bind_api(self, action="merchant_tax_rate", merchant_id=merchant_id,  tax_id=tax_id, expand=expand)

	@merchant_id_required
	@auth_token_required
	#returns all categories for a merchant
	def merchant_categories(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_categories", filter_by=filter_by, expand=expand)

	@merchant_id_required
	@category_id_required
	@auth_token_required
	#returns a category based on the category id
	def merchant_category(self, merchant_id=None, category_id=None, filter_by=None):
		return bind_api(self, action="merchant_category", merchant_id=merchant_id, category_id=category_id, filter_by=None)

	@merchant_id_required
	@category_id_required
	@auth_token_required
	def items_in_category(self, merchant_id=None, category_id=None, filter_by=None, expand=None):
		return bind_api(self, merchant_id=merchant_id, category_id=category_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@item_id_required
	@auth_token_required
	#get all categories for a single item.
	def item_categories(self, merchant_id=None, item_id=None, filter_by=None, expand=None):
		return bind_api(self, action="categories_for_item", merchant_id=merchant_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@tax_id_required
	@auth_token_required
	def merchant_items_by_tax_rate(self, merchant_id=None, tax_id=None, filter_by=None, expand=None):
		return bind_api(action="items_by_tax_rate", merchant_id=merchant_od, tax_id=tax_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@auth_token_required
	#returns all merchant modifier groups
	def merchant_modifier_groups(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_modifier_groups", merchant_id=merchant_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@auth_token_required
	#returns all modifiers for a merchant
	def merchant_modifiers(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_get_modifiers", filter_by=filter_by, expand=expand)

	@merchant_id_required
	@modifier_group_id_required
	@auth_token_required
	#returns all modifiers for a modifier group id
	def merchant_modifiers_for_modifier_group(self, merchant_id=None, modifier_group_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_get_modifiers_for_group", merchant_id=merchant_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@modifier_group_id_required
	@modifier_id_required
	@auth_token_required
	#returns a single modifier within a group
	def merchant_modifier(self, merchant_id=None, modifier_group_id=None, modifier_id=None, expand=None):
		return bind_api(self, action="merchant_get_modifier", merchant_id=merchant_id, modifier_id=modifier_id, expand=expand)

	@merchant_id_required
	@auth_token_required
	#retuns all merchant attributes
	def merchant_attributes(self, merchant_id=None, filter_by=None):
		return bind_api(self, action="merchant_get_attributes", merchant_id=merchant_id, filter_by=filter_by)

	@merchant_id_required
	@attribute_id_required
	@auth_token_required
	#returns a specific attribute based on the attribute id
	def merchant_attribute(self, merchant_id=None, attribute_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_attribute", merchant_id=merchant_id, attribute_id=attribute_id, filter_by=filter_by, expand=expand)
	
	@merchant_id_required
	@auth_token_required
	#returns all options for a merchant

	def merchant_options(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_options", merchant_id=merchant_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@attribute_id_required
	@option_id_required
	@auth_token_required
	#returns a single option based on the option id

	def merchant_options_for_attribute(self, merchant_id=None, attribute_id=None, filter_by=None, option_id=None,  expand=None):
		return bind_api(self, action="merchant_get_option_for_attribute", merchant_id=merchant_id, option_id=option_id, attribute_id=attribute_id, filter_by=filter_by, expand=expand)	


	@merchant_id_required
	@auth_token_required
	#returns the orders for a merchant
	def merchant_orders(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_orders", merchant_id=merchant_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@order_id_required
	@auth_token_required
	def merchant_order(self, merchant_id=None, order_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_order", merchant_id=merchant_id, order_id=order_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@order_id_required
	@auth_token_required

	#returns all discounts for an order
	def merchant_discounts_for_order(self, merchant_id=None, order_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_discounts_for_order", merchant_id=merchant_id, order_id=order_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@order_id_required
	@discount_id_required
	@auth_token_required
	#returns a single discount for a single order

	def merchant_discount_for_order(self, merchant_id=None, order_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_discount_for_order", merchant_id=merchant_id, order_id=order_id, discount_id=discount_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@order_id_required
	@auth_token_required
	#returns all line items for an order

	def merchant_line_items_for_order(self, merchant_id=None, order_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_line_items_for_order", merchant_id=merchant_id, order_id=order_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@order_id_required
	@line_item_id_required
	@auth_token_required
	#returns a single line item for an order based on the line item id

	def merchant_line_item_for_order(self, merchant_id=None, line_item_id=None, order_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_line_items_for_order", merchant_id=merchant_id, line_item_id=line_item_id, order_id=order_id, filter_by=filter_by, expand=expand)


	@merchant_id_required
	@auth_token_required
	#returns all authorizations for a merchant
	def merchant_authorizations(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_authorizations", merchant_id=merchant_id, filter_by=filter_by, expand=expand)


	@merchant_id_required
	@auth_id_required
	@auth_token_required
	#returns a single authorization for a merchant
	def merchant_authorzation(self, merchant_id=None,  auth_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_authorization", merchant_id=merchant_id, order_id=order_id, filter_by=filter_by, expand=expand)


	@merchant_id_required
	@auth_token_required
	#returns all payments for a merchant
	def merchant_payments(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_payments", merchant_id=merchant_id, filter_by=filter_by, expand=expand)



	@merchant_id_required
	@pay_id_required
	@auth_token_required

	#returns a single payment for a merchant based on the pay id
	def merchant_payment(self, merchant_id=None, pay_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_payment", merchant_id=merchant_id, pay_id=order_id, filter_by=filter_by, expand=expand)


	@merchant_id_required
	@order_id_required
	@auth_token_required
	#returns all payments for an order

	def merchant_payments_for_order(self, merchant_id=None, order_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_payments_for_order", merchant_id=merchant_id, order_id=order_id, filter_by=filter_by, expand=expand)


	@merchant_id_required
	@employee_id_required
	@auth_token_required
	#returns all payments under an employee

	def merchant_payments_for_employee(self, merchant_id=None, employee_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_payments_for_employee", merchant_id=merchant_id, employee_id=employee_id, filter_by=filter_by, expand=expand)


	@merchant_id_required
	@auth_token_required
	#returns all refunds for a merchant
	def merchant_refunds(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_refunds", merchant_id=merchant_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@refund_id_required
	@auth_token_required
	#returns a single refund based on the refund id

	def merchant_refund(self, merchant_id=None, refund_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_refund", merchant_id=merchant_id, refund_id=refund_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@auth_token_required
	#returns all credits for a merchant
	def merchant_credits(self, merchant_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_credits", merchant_id=merchant_id, filter_by=filter_by, expand=expand)

	@merchant_id_required
	@credit_id_required
	@auth_token_required
	#returns a single credit based on the credit id

	def merchant_credit(self, merchant_id=None, credit_id=None, filter_by=None, expand=None):
		return bind_api(self, action="merchant_credit", merchant_id=merchant_id, credit_id=credit_id, filter_by=filter_by, expand=expand)


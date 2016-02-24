import requests
from headers import (
	get_headers_generic,
	get_headers_authorization	
)
from cloverExceptions import cloverException



def get_base_endpoint(action):
	if action.__contains__("merchant"):
		return "https://api.clover.com:443/v3/merchants/{}/"


def bind_api(
	self,
	action=None,
	auth_id=None,
	auth_token=None,
	attribute_id=None,
	body=None,
	category_id=None,
	credit_id=None,
	developer_id=None,
	discount_id=None,
	device_id = None,
	employee_id=None,
	expand=None,
	filter_by=None,
	item_id=None,
	item_group_id=None,
	line_item_id=None,
	merchant_id=None,
	modifier_id=None,
	modifier_group_id=None,
	fields=None,
	option_id=None,
	order_type_id=None,
	pay_id=None,
	refund_id=None,
	role_id=None,
	shift_id=None,
	tax_id=None,
	tag_id=None,
	tip_id=None,
	tender_id=None,
	return_json = False,

	):
	#merchant functions
	BASE_ENDPOINT = get_base_endpoint(action)
	try:
		headers = get_headers_authorization(self.auth)
	except:
		headers = get_headers_generic()
	
	if action == "merchant":
		print merchant_id
		#api reference = https://www.clover.com/api_docs#!/merchants/GetMerchant
		response =  requests.get(
			BASE_ENDPOINT.format(merchant_id),
			headers=headers)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)


	elif action == "update_merchant":
		#api reference = https://www.clover.com/api_docs#!/merchants/UpdateMerchant
		response = requests.post(
			BASE_ENDPOINT.format(merchant_id),
			headers=headers,
			data=fields if fields else None,
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason:{}".format(response.status_code, response.reason)


	elif action == "merchant_address":
		#api reference = https://www.clover.com/api_docs#!/merchants/GetMerchantAddress
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id) + "address",
			headers=headers
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_properties":
		#api reference = https://www.clover.com/api_docs#!/merchants/GetMerchantProperties
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id) + "properties",
			headers=headers
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)




	elif action == "update_merchant_properties":
		#api reference = https://www.clover.com/api_docs#!/merchants/UpdateMerchantProperties
		pass

	elif action == "merchant_plan":
		#api reference = https://www.clover.com/api_docs#!/merchants/UpdateMerchantPlan
		response = requests.post(
			BASE_ENDPOINT.format(merchant_id)+"plan",
			headers=headers,
			data=body if body else None 
			)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "default_service_charge":
		#api reference = https://www.clover.com/api_docs#!/merchants/GetDefaultServiceCharge
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"default_service_charge",
			headers = headers

		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)


	elif action == "merchant_tip_suggestions":
		#api reference = https://www.clover.com/api_docs#!/merchants/GetTipSuggestions
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"tip_suggesstions",
			headers=headers
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_tip_suggestion":
		#api reference = https://www.clover.com/api_docs#!/merchants/GetTipSuggestion
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"tip_suggestion"+"/{}".format(tip_id),
			headers = headers,
		)
		if response.status_code == response.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "update_merchant_tip_suggestion":
		#api reference = https://www.clover.com/api_docs#!/merchants/UpdateTipSuggestion
		pass


	elif action == "all_merchant_order_types":
		#api reference = https://www.clover.com/api_docs#!/merchants/GetOrderTypes
		pass

	elif action == "create_merchant_order_types":
		#api reference = https://www.clover.com/api_docs#!/merchants/CreateOrderType
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"order_types",
			headers = headers
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "get_merchant_order_type":
		#api reference = https://www.clover.com/api_docs#!/merchants/GetOrderType
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"order_types"+"/{}".format(order_type_id),
			headers = headers
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "update_merchant_order_type":
		#api reference = https://www.clover.com/api_docs#!/merchants/UpdateOrderType
		pass

	elif action == "delete_merchant_order_type":
		#api reference = https://www.clover.com/api_docs#!/merchants/UpdateOrderType
		pass

	elif action == "create_merchant_type_category":
		#api reference = https://www.clover.com/api_docs#!/merchants/DeleteOrderType
		pass

	elif action == "delete_merchant_type_category":
		#api reference = https://www.clover.com/api_docs#!/merchants/CreateOrDeleteOrderTypeCategories
		pass

	elif action == "list_system_order_types":
		#api reference = https://www.clover.com/api_docs#!/merchants/GetSystemOrderTypes
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"system_order_types",
			headers=headers
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "roles":
		#api reference = https://www.clover.com/api_docs#!/merchants/GetRoles
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"roles",
			headers = headers
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "create_role_for_merchant":
		#api reference = https://www.clover.com/api_docs#!/merchants/CreateRole
		pass

	elif action == "get_role_for_merchant":
		#api reference = https://www.clover.com/api_docs#!/merchants/GetRole
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"roles/{}/".format(role_id)
		)
		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "update_role_for_merchant":
		#api reference = https://www.clover.com/api_docs#!/merchants/UpdateRole
		pass

	elif action == "delete_role_for_merchant":
		#api reference = https://www.clover.com/api_docs#!/merchants/DeleteRole
		pass

	elif action == "merchant_tenders":
		#api reference = https://www.clover.com/api_docs#!/merchants/GetMerchantTenders
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"tenders",
			headers = headers,
			json=filter_by
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_tender":
		#api reference = https://www.clover.com/api_docs#!/merchants/GetMerchantTender
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"tenders/{}/".format(tender_id)
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_opening_hours":
		#api reference = https://www.clover.com/api_docs#!/merchants/GetAllMerchantOpeningHours
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"opening_hours",
			headers=headers
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "create_merchant_opening_hours":
		#api reference = https://www.clover.com/api_docs#!/merchants/CreateMerchantOpeningHours
		pass

	elif action == "specific_merchant_opening_hours":
		#api reference = https://www.clover.com/api_docs#!/merchants/GetMerchantOpeningHours
		pass

	elif action == "update_merchant_opening_hours":
		#api reference = https://www.clover.com/api_docs#!/merchants/UpdateMerchantOpeningHours
		pass

	elif action == "delete_merchant_opening_hours":
		#api reference = https://www.clover.com/api_docs#!/merchants/DeleteMerchantOpeningHours
		pass

	#end of merchant functions

	#cash functions
	if action == "merchant_cash_events":
		#api reference = https://www.clover.com/api_docs#!/cash/GetAllCashEvents
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id) +"cash_events",
			headers=headers,
			json=filter_by if filter_by else expand

		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_employee_cash_events":
		#api reference = https://www.clover.com/api_docs#!/cash/GetEmployeeCashEvents
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id) +"employees/{}/cash_events".format(employee_id),
			headers = headers,
			json=filter_by if filter_by else expand

		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchants_devices_cash_events":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"devices/{}/cash_events".format(device_id),
			headers = headers,
			json=filter_by if filter_by else expand
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)


	#end of cash functions

	#customer functions

	elif action == "merchant_customers_as_csv":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id) +"customers.csv",
			headers=headers,
			json=filter_by if filter_by else expand
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_customers":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id) +"customers",
			headers=headers,
			json=filter_by if filter_by else expand
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)


	elif action == "merchant_customer":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"customers/{}".format(customer_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code:: {}, reason: {}".format(response.status_code, response.reason)

	#end of customer functions

	#employee functions

	elif action == "merchant_employees":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"employees",
			headers=headers,
			json=filter_by if filter_by else expand

		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_employee":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"employees/{}".format(employee_id),
			headers=headers,
			json=expand,
		)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	#end of employee functions

	#shift functions
	elif action == "merchant_shifts":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"shifts",
			headers=headers,
			json=filter_by
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_shift":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"shifts/{}".format(shift_id),
			headers=headers,
			json=expand
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_shifts_as_csv":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"shifts/{}".format(shift_id),
			headers=headers,
			json=expand
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_employee_shifts":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"employees/{}/shifts".format(employee_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_employee_shift":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"employees/{}/shifts/{}".format(employee_id, shift_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)


	elif action == "merchant_employee_orders":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"employees/{}/orders".format(employee_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)
	#end of shift function

	#inventory functions

	elif action == "merchant_inventory_items":
		response = requests.get(
			BASE_ENDPOINT.format(me4chant_id)+"items",
			headers=headers,
			json=filter_by if filter_by else expand
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_inventory_item":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"items/{}".format(employee_id, item_id),
			headers=headers,
			json=expand
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_item_stocks":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"item_stocks",
			headers=headers,

		)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_item_stock":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"item_stocks/{}".format(item_id),
			headers=headers,

		)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_item_groups":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"item_groups",
			headers=headers,

		)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_item_group":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"item_groups/{}".format(item_group_id),
			headers=headers,
			json=expand,

		)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_tags":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"tags",
			headers=headers,
			json=filter_by if filter_by else expand

		)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_tag":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"tags/{}".format(tag_id),
			headers=headers,
			json=expand

		)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_item_tags":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"items/{}/tags".format(item_id),
			headers=headers,
			json=filter_by if filter_by else expand

		)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_items_for_tag":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"tags/{}/items".format(tag_id),
			headers=headers,
			json=filter_by if filter_by else expand

		)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_tax_rates":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"tax_rates",
			headers=headers,
			json=filter_by if filter_by else expand

		)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_tax_rate":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"tax_rates/{}".format(tax_id),
			headers=headers,
			json=expand

		)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_categories":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"categories",
			headers=headers,
			json=filter_by if filter_by else expand

		)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_category":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"categories/{}".format(category_id),
			headers=headers,
			json=filter_by
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "items_in_category":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"categories/{}/items".format(category_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "categories_for_item":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"items/{}/categories".format(item_id),
			headers=headers,
			json=filter_by if filter_by else expand

		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "items_by_tax_rate":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"tax_rates/{}/items".format(tax_id),
			headers=headers,
			json=filter_by if filter_by else expand

		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)


	elif action == "merchant_modifier_groups":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"modifier_groups",
			headers=headers,
			json=filter_by if filter_by else expand

		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action== "merchant_get_modifiers":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"modifiers",
			headers=headers,
			json=filter_by if filter_by else expand
		)

	elif action == "merchant_get_modifier_for_group":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"modifier_groups/{}/modifiers",
			headers=headers,
			json=filter_by if filter_by else expand,
		)

	elif action == "merchant_get_modifier":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"modifier_groups/{}/modifiers/{}".format(modifier_group_id, modifier_id)
		)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_get_attributes":
		response = requests.get(
			BASE_ENDPOINTS.format(merchant_id)+"attributes",
			headers=headers,
			json=filter_by
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_attribute":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"attributes/{}".format(attribute_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)
	elif action == "merchant_options":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"options",
			headers=headers,
			json=filter_by if filter_by else expand,
		)

		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_get_option_for_attribute":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"attributes/{}/options/{}".format(attribute_id, option_id)
		)

	#end of inventory functions

	#order functions

	elif action == "merchant_orders":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"orders",
			headers=headers,
			params=filter_by if filter_by else expand
		)
		if response.status_code == requests.codes.ok:
			return response.json();

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)


	elif action == "merchant_order":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"orders/{}".format(order_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_discounts_for_order":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"orders/{}/discounts".format(order_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_discount_for_order":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"orders/{}/discounts/{}".format(order_id, discount_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	

	elif action == "merchant_line_items_for_order":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"orders/{}/line_items/".format(order_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)


	
	elif action == "merchant_line_item_for_order":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"orders/{}/line_items/{}".format(order_id, line_item_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	#end of order functions

	#payment functions

	elif action == "merchant_authorizations":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"authorizations",
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_authorization":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"authorizations/{}".format(auth_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)



	elif action == "merchant_payments":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"payments",
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_payment":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"payments/{}".format(pay_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_payments_for_order":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"orders/{}/payments/".format(order_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)
	
	elif action == "merchant_payments_for_employee":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"employees/{}/payments/".format(employee_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)
	
	elif action == "merchant_refunds":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"refunds/",
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)
	
	elif action == "merchant_refund":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"refunds/{}".format(refund_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_credits":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"credits/",
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)

	elif action == "merchant_credit":
		response = requests.get(
			BASE_ENDPOINT.format(merchant_id)+"credits/{}".format(credit_id),
			headers=headers,
			json=filter_by if filter_by else expand
		)

		if response.status_code == requests.codes.ok:
			return response.json()

		else:
			return "code: {}, reason: {}".format(response.status_code, response.reason)
	#end of payment functions
	


























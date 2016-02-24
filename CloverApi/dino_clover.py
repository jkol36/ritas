import cherrypy
import requests
import json
import dateutil.parser
import hashlib
import xml.etree.ElementTree as ET
from xml.dom import minidom

from sqlalchemy import *
from sqlalchemy.orm import joinedload, sessionmaker
from sqlalchemy.sql.expression import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased

import calendar
import dateutil.parser
import os
import smtplib
import time
import traceback
import urllib2
from datetime import date, datetime, timedelta
from decimal import Decimal
from glob import glob
from os import listdir, remove
# from db.clover import Order, OrderAdjustment, LineItem, LineItemAdjustment, LineItemModification, Payment, PaymentCard, PaymentTax, ProductSizes, Refund, Credit, Status, OrderStatus
# from db.pos import PaymentType
# from db.product import ProductType, ProductSize
# from db.store import Store, CloverInfo
# from db.tz import Timezone, DSTWindow
# from lib.crypto import enc_aes, dec_aes
# from lib.dt import decstring, isostring, moneystring
# from lib.util import is_production, appropriate_service_host, appropriate_error_mailbox, appropriate_donotreply_mailbox
from socket import gethostname

# declare where XML files are staged
xmldirectory = "xml/"

productalias = {	'11'			:	'109',
			'12'			:	'110',
			'13'			:	'111',
			'44'			:	'109',
			'45'			:	'110',
			'46'			:	'111',
			'FD_VARIABLE_GIFTCARDS'	:	'180'}

# class Query(object):

# 	@cherrypy.expose
# 	#@cherrypy.tools.sa()
# 	@cherrypy.tools.json_out()
# 	@cherrypy.tools.json_in()
# 	@cherrypy.tools.validate_hmac( keyname='clover' )
#         def lookupByStoreID(self):
#                 j=cherrypy.request.json
#                 session = cherrypy.request.db.coolnet
#                 try:
#                         s = session.query(CloverInfo).filter(CloverInfo.storeid == j['store']).one()
#                         return dict(api = s.apikey, activateraw = isostring(s.activationtimestamp))
#                 except:
#                         return []

# 	@cherrypy.expose
# 	@cherrypy.tools.sa()
# 	@cherrypy.tools.json_out()
# 	@cherrypy.tools.json_in()
# 	@cherrypy.tools.validate_hmac( keyname='clover' )
#         def lookupByToken(self):
#                 j = cherrypy.request.json
#                 if 'api' in j:
#                         url = 'https://api.clover.com/v3/merchants/current?access_token=' + str(j['api'])
#                         req = requests.get(url)
#                         return dict(id = req.json()['id'] if 'id' in req.json() else 'BAD API TOKEN')
#                 else:
#                         return dict(id = '')
# class Send(object):

# 	def _notify_cannot_send_xml(self, error_details, filename):
# 		print '_notify_cannot_send_xml: %s' % error_details
# 		s = smtplib.SMTP('localhost')
# 		tpl = """MIME-Version:1.0
# Content-type: text/html
# From: %s
# To: %s
# Subject: (%s:%s) Error sending staged XML file %s
# <pre>%s</pre>"""
# 		frm = appropriate_donotreply_mailbox()
# 		to = appropriate_error_mailbox()
# 		s.sendmail (frm, [to], tpl % (frm,to,gethostname(),cherrypy.server.socket_port,filename,error_details) )

# 	@cherrypy.expose
# 	@cherrypy.tools.sa()
# 	@cherrypy.tools.json_out()
# 	@cherrypy.tools.validate_hmac( keyname='clover' )
# 	def stagedFiles(self):
# 		cherrypy.response.timeout = 360000
# 		session = cherrypy.request.db.coolnet
# 		files = listdir(xmldirectory)
# 		if len(files):
# 			s = session.query(CloverInfo).options(joinedload(CloverInfo.store)).all()
# 			ritasid_lookup = dict()
# 			for store in s:
# 				ritasid_lookup[store.store.ritasid] = store.storeid
# 			for item in files:
# 				try:
# 					filepath = os.path.abspath(xmldirectory+item) # using abspath guarantees that sp-pos can get and access the file
# 					salesfile = open(filepath, 'r')
# 					content = salesfile.read()
# 					parsed = ET.XML(content)
# 					outlet = parsed.find('outlet')
# 					outletid = outlet.find('id').text
# 					registerid = outlet.find('registerid').text
# 					salesfile.close()

# 					# this call guarantees that the call reaches the appropriate sp-pos instance/dir
# 					from lib.key import KeyManager
# 					path = '/pos_process/file_queue/add'
# 					km = KeyManager()
# 					port = 9081
# 					data = '{"ritasid":"%s", "register":"%s", "xmlpath":"%s", "storeid":"%s"}' % (outletid, registerid, filepath, str(ritasid_lookup[outletid]))
# 					url = 'http://%s:%s%s' % (appropriate_service_host(), port, path)
# 					d = isostring(datetime.now())
# 					auth_headers = km.auth_headers('pos_process', d, path)
# 					request = urllib2.Request(url, headers=auth_headers)
# 					req = urllib2.urlopen(request, data)
# 					ret = req.read()
# 				except:
# 					self._notify_cannot_send_xml(repr(traceback.format_exc()), item)
# 					continue

class Stage(object):

	def _checkDSTWindow(self,dstwindow, orderdate):
		windowstart = date(datetime.now().year, dstwindow['startmonth'], 1)
		if windowstart.isoweekday() != dstwindow['startisoday']:
			windowstart = self._nextWeekday(windowstart, dstwindow['startisoday'])
		if windowstart.isoweekday() == dstwindow['startisoday'] and dstwindow['startdayinmonth'] > 1:
			windowstart = windowstart + timedelta(7 * (dstwindow['startdayinmonth'] - 1))

		windowend = date(datetime.now().year, dstwindow['endmonth'], 1)
		if windowend.isoweekday() != dstwindow['endisoday']:
			windowend = self._nextWeekday(windowend, dstwindow['endisoday'])
		if windowend.isoweekday() == dstwindow['endisoday'] and dstwindow['enddayinmonth'] > 1:
			windowend = windowend + timedelta(7 * (dstwindow['enddayinmonth'] - 1))

		orderdate = dateutil.parser.parse(orderdate).date()

		return (orderdate >= windowstart and orderdate <= windowend)

	def _epochToDatetime(self,milliseconds,offset=None):
		return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime((milliseconds/1000) + (0 if not offset else offset)))

	def _findTimezone(self,timezones,tz):
		index = 0
		found = False
		for zone in timezones:
			if zone.Timezone.countryname == tz:
				found = True
				break
			index += 1
		return index if found else None

	def _getLocalTime(self,timezones,dstwindow,ordertimezone,paymenttimestamp):
		# need to get the offset for this tz
		index = self._findTimezone(timezones,ordertimezone)
		current_offset = dict(utc=(timezones[index].Timezone.utcminutesoffset*60), dst=(timezones[index].Timezone.dstminutesoffset*60))

		timestamp = self._epochToDatetime(paymenttimestamp)
		clienttimestampUTC = self._epochToDatetime(paymenttimestamp,current_offset['utc'])
		clienttimestampDST = self._epochToDatetime(paymenttimestamp,current_offset['dst'])

		isDST = self._checkDSTWindow(dstwindow,clienttimestampUTC)
		clienttimestamp = clienttimestampDST if isDST else clienttimestampUTC
		clientdatetime_obj = dateutil.parser.parse(clienttimestamp)

		return current_offset, isDST, clientdatetime_obj

	def _getPaymentType(self, payment_types, tender):
		result = tender
		for paymenttype in payment_types:
			if tender in paymenttype['name'].split(','):
				result = paymenttype['id']
		return result

	def _init_file_data(self, payment_types, timezones, sales_date, file_data):
		dstwindow = dict(startmonth=timezones[0].startmonth, startisoday=timezones[0].startisoday, startdayinmonth=timezones[0].startdayinmonth, endmonth=timezones[0].endmonth, endisoday=timezones[0].endisoday, enddayinmonth=timezones[0].enddayinmonth)
		result = dict(orders=[],taxrates=[])
		order_index = 0
		for order in file_data['orders']:
			order_index += 1
			# get the full order details
			data = self._order_details(order, payment_types)
			# skip this order if we can't get valid items
			if not data:
				continue
			if not len(data['payments']):
				continue
			paymenttimestamp = data['payments'][0]['timestamp']
			current_offset, isDST, clientdatetime_obj = self._getLocalTime(timezones,dstwindow,file_data['timezone'],paymenttimestamp)

			if clientdatetime_obj.date() != sales_date:
				continue

			# need the clienttimestamp formatted to ISO standard for use in XML file
			clientoffset = (current_offset['dst'] if isDST else current_offset['utc']) / 60
			hoursoffset = clientoffset / 60
			minutesoffset = clientoffset % 60
			timezone = '%+03d:%02d'%(hoursoffset, minutesoffset)
			isodatetime = clientdatetime_obj.isoformat()+timezone
			orderdate = clientdatetime_obj.date()

			# create a map of tax rates for this day, need to make sure all tax amounts fall into the right tax "bucket" for SMART
			for rate in data['tax'].keys():
				if rate not in result['taxrates']:
					result['taxrates'].append(rate)

			result['timezone'] = timezone
			if 'currency' not in result and 'currency' in order:
				result['currency'] = order['currency']

			data['id'] = str(order_index)
			data['clover_id'] = order['id']
			data['datetime'] = isodatetime[:-6]
			data['drawer'] = '1' # Not sure if this references register or separate cash till, default to 1

			result['orders'].append(data)

		# tax rates can be tricky, we created a map above of all tax rates on a day/store basis; make sure the tax amounts fall into the right "buckets"
		taxrates = sorted(result['taxrates'], reverse=True)
		for order in result['orders']:
			if len(taxrates) == 0:
				order['taxes'] = []
				continue
			taxes = []
			taxes.append('0.00' if taxrates[0] not in order['tax'] else order['tax'][taxrates[0]])
			tax2 = Decimal(0)
			for rate in order['tax'].keys():
				tax2 += Decimal(order['tax'][rate]) if rate != taxrates[0] else Decimal(0)
			if tax2 > 0:
				taxes.append(moneystring(tax2))
			order['taxes'] = taxes
		return result

	def _initPaymentTypes(self):
		session = cherrypy.request.db.coolnet
		p = session.query(PaymentType).order_by(PaymentType.id).all()
		return [dict(id=type.id, name=type.clovertender) for type in p]

	def _initTimezones(self):
		session = cherrypy.request.db.coolnet
		timezones = session.query(Timezone)\
				.join(DSTWindow, DSTWindow.countrycode == Timezone.countrycode)\
				.add_column(DSTWindow.startmonth)\
				.add_column(DSTWindow.startisoday)\
				.add_column(DSTWindow.startdayinmonth)\
				.add_column(DSTWindow.endmonth)\
				.add_column(DSTWindow.endisoday)\
				.add_column(DSTWindow.enddayinmonth)\
				.filter(Timezone.countrycode == 'US').all()
		return timezones

	def _nextWeekday(self, d, isoweekday):
		days_ahead = isoweekday - d.isoweekday()
		return d + timedelta(days_ahead)

	def _notify_cannot_parse_json(self, error_details, bad_json, storeid, ritasid, salesdate):
		print '_notify_cannot_parse_json: %s' % error_details
		s = smtplib.SMTP('localhost')
		tpl = """MIME-Version:1.0
Content-type: text/html
From: %s
To: %s
Subject: (%s:%s) Error parsing JSON returned by Clover API for Store %s (intStoreID %s) with sales from %s
<h3>TRACEBACK:</h3>
<pre>%s</pre>
<h3>RAW JSON:</h3>
<pre>%s</pre>"""
		frm = appropriate_donotreply_mailbox()
		to = appropriate_error_mailbox()
		s.sendmail (frm, [to], tpl % (frm,to,gethostname(),cherrypy.server.socket_port,ritasid,storeid,salesdate,error_details,bad_json) )

	def _notify_cannot_write_xml(self, error_details, ritasid, salesdate):
		print '_notify_cannot_write_xml: %s' % error_details
		s = smtplib.SMTP('localhost')
		tpl = """MIME-Version:1.0
Content-type: text/html
From: %s
To: %s
Subject: (%s:%s) Error staging XML file for Store %s with sales from %s
<pre>%s</pre>"""
		frm = appropriate_donotreply_mailbox()
		to = appropriate_error_mailbox()
		s.sendmail (frm, [to], tpl % (frm,to,gethostname(),cherrypy.server.socket_port,ritasid,salesdate,error_details) )

	def _order_details(self, order, payment_types):
                session = cherrypy.request.db.coolnet

		lineitems = []
		#total sale - discount(which is tax)
		totalcache = Decimal(0)
		for lineitem in order['lineItems']['elements']:
			try:
				productsize = int(productalias[lineitem['item']['code']]) if lineitem['item']['code'] in productalias else int(lineitem['item']['code'])
				# we need to make sure that all lineitems can be mapped to CoolNet products
				# the goal here is to make sure query().one() does not throw an exception!
				ps = session.query(ProductSize)\
					.options(joinedload(ProductSize.producttype))\
					.filter(ProductSize.id == productsize).one()
				price = Decimal(lineitem['price'])/100
				totalsale = price
				discounts = []
				if 'discounts' in lineitem:
					for discount in lineitem['discounts']['elements']:
						amount = discount['percentage'] if 'amount' not in discount else Decimal(abs(discount['amount']))/100
						percent = ('percentage' in discount)
						if percent:
							totalsale -= price * Decimal(moneystring(Decimal(amount)))/100 # need to force rounding on percentages, then re-parse into Decimal object
						else:
							totalsale -= amount
						discounts.append(dict(amount=str(amount) if percent else moneystring(amount),
									percent=str(int(percent)),
									coupon='-1')) # not sure yet how to map discounts to CoolNet discount coupons, default to -1 for 'ignore'
				totalcache += Decimal(moneystring(totalsale))
				lineitems.append(dict(productsize=str(productsize),
							producttype=str(ps.producttypeid),
							nonproduct=str(int(ps.producttype.isnonproduct)),
							quantity='1',
							totalsale=moneystring(price),
							nontax=str(0 if 'taxRemoved' not in order else int(order['taxRemoved'])),
							discounts=discounts))
			except:
				return None

		# if this order is valid, and all lineitems are valid, we are clear to process discounts, payment info, etc
		orderdiscounts = Decimal(0)
		discounts = []
		if 'discounts' in order:
			for discount in order['discounts']['elements']:
				amount = discount['percentage'] if 'amount' not in discount else Decimal(abs(discount['amount']))/100
				percent = ('percentage' in discount)
				if percent:
					orderdiscounts += (totalcache * Decimal(moneystring(Decimal(amount)))/100) if amount is not None else 0 # need to force rounding on percentages, then re-parse into Decimal object
				else:
					orderdiscounts += amount
				discounts.append(dict(amount=str(amount) if percent else moneystring(amount),
							percent=str(int(percent)),
							coupon='-1')) # not sure yet how to map discounts to CoolNet discount coupons, default to -1 for 'ignore'
		totalcache -= Decimal(moneystring(orderdiscounts))

		payments = []
		taxes = {}
		for payment in order['payments']['elements']:
			for tax in payment['taxRates']['elements']:
				rate = Decimal(tax['rate'])/10000000
				taxpaid = Decimal(moneystring(Decimal(tax['taxableAmount'])/100 * rate))
				taxes[decstring(rate)] = moneystring(Decimal(taxes[decstring(rate)]) + taxpaid) if decstring(rate) in taxes else moneystring(taxpaid)
			taxamount = Decimal(payment['taxAmount'])/100
			totalcache += taxamount
			payments.append(dict(amount=moneystring(Decimal(payment['amount'])/100),
						taxamount=moneystring(taxamount),
						paymenttype=str(self._getPaymentType(payment_types, payment['tender']['label'])),
						timestamp=payment['clientCreatedTime'] ))

		staffid = '1' if 'employee' not in order else str(int(hashlib.sha256(order['employee']['id']).hexdigest(),base=16))[:4] # since Clover gives us a hashed value, we turn it into a number

		return dict(staffid=staffid,
				taxexempt=(None if 'taxRemoved' not in order else str(int(order['taxRemoved']))),
				totalcache=moneystring(totalcache),
				tax=taxes,
				lineitems=lineitems,
				payments=payments,
				discounts=discounts)

	def _prettify(self, elem):
		rough_string = ET.tostring(elem, 'utf-8')
		reparsed = minidom.parseString(rough_string)
		return reparsed.toprettyxml(indent="	")

	def _pull_from_clover(self, stores=None, startday=None, endday=None, payment_types=None, timezones=None):
                session = cherrypy.request.db.coolnet
		now = datetime.now()
		if startday == None:
			startday = datetime(now.year, now.month, now.day, 8)
		if endday == None:
			endday = datetime(now.year, now.month, now.day, 8)
		if startday.date() > endday.date():
			raise Exception('startdate greater than enddate')

		delta = endday - startday

		s = session.query(CloverInfo)
		if stores:
			s = s.filter(CloverInfo.storeid.in_(stores))
		s = s.options(joinedload(CloverInfo.store)).all()

		result = dict()

		for store in s:
			# need to create key and decrypt stored MerchantID value
			salt = str(store.storeid)
			merchantid = dec_aes(store.merchantid,hashlib.md5(salt).digest())

			# merchant timezone used to be returned in the orders dataset, now need to explicitly pull this information
			merchant_url = 'https://api.clover.com/v3/merchants/{merchantid}/properties?access_token={access_token}&limit=1000'.format(merchantid=merchantid, access_token=store.apikey)
			merchant_req = requests.get(merchant_url, headers = {'Accept':'application/json', 'Content-type':'application/json'})
			try:
				merchant = merchant_req.json()
			except:
				self._notify_cannot_parse_json(repr(traceback.format_exc()), merchant_req.text, store.storeid, store.store.ritasid, isostring(startday.date()))
				continue

			for i in range(0, delta.days+1):
				day = startday + timedelta(days=i)
				end = day + timedelta(days=1)

				if day.date() < store.activationtimestamp.date():
					continue

				day_key = isostring(day.date())

				expand_components = ['payments.taxRates','payments.tender','lineItems.items','lineItems.discounts','discounts']
				url = 'https://api.clover.com/v3/merchants/{merchantid}/orders'\
					+ '?expand='+'%2C'.join(expand_components)\
					+ '&filter=clientCreatedTime%3E={starttime}&filter=clientCreatedTime%3C={endtime}&filter=testMode%3Dfalse'\
					+ '&limit=1000&access_token={access_token}&orderBy=clientCreatedTime%20ASC'
				url = url.format(merchantid=merchantid, starttime=str(calendar.timegm(day.timetuple())*1000), endtime=str(calendar.timegm(end.timetuple())*1000), access_token=str(store.apikey))
				req = requests.get(url, headers = {'Accept':'application/json', 'Content-type':'application/json'})
				try:
					o = req.json()
				except:
					self._notify_cannot_parse_json(repr(traceback.format_exc()), req.text, store.storeid, store.store.ritasid, day_key)
					continue
				if len(o['elements']) == 0:
					continue
				if day_key not in result:
					result[day_key] = dict()
				result[day_key][store.storeid] = dict(storenumber=store.store.ritasid, storeid=store.store.id, timezone=merchant['timezone'], orders=[])
				for order in o['elements']:
					if ('isDeleted' in order and order['isDeleted'] == True) or ('testMode' in order and order['testMode'] == True) or ('state' in order and order['state'] != 'locked'):
						continue
					else:
						if len(order['lineItems']['elements']) == 0:
							continue
						result[day_key][store.storeid]['orders'].append(order)

				try:
					file_data = self._init_file_data(payment_types, timezones, day.date(), result[day_key][store.storeid])
					file_data['salesdate'] = day_key
					file_data['storeid'] = str(store.storeid)
					file_data['outletid'] = str(store.store.ritasid)
					if 'timezone' not in file_data:
						file_data['timezone'] = '-04:00'
					if 'currency' not in file_data:
						file_data['currency'] = 'USD'
					file_data['registerid'] = '1' # until multiple registers are supported and the proper structure is determined, use declared variable here
					self._write_xml(file_data)
				except:
					continue
		return True


	def _write_xml(self, file_data):
		try:
			generated_on = datetime.now().isoformat()
			root = ET.Element('postran')
			trandatetime = ET.SubElement(root, 'datetime')
			trandatetime.text = generated_on
			timezone = ET.SubElement(root, 'timezone')
			timezone.text = file_data['timezone']
			coolposversion = ET.SubElement(root, 'coolposversion')
			coolposversion.text = 'CLOVER'
			outlet = ET.SubElement(root, 'outlet')

			outletid = ET.SubElement(outlet, 'id')
			outletid.text = file_data['outletid']
			currency = ET.SubElement(outlet, 'currency')
			currency.text = file_data['currency']
			outlettz = ET.SubElement(outlet, 'timezone')
			outlettz.text = file_data['timezone']
			registerid = ET.SubElement(outlet, 'registerid')
			registerid.text = file_data['registerid']

			for order in file_data['orders']:
				o = ET.SubElement(outlet, 'order')
				id = ET.SubElement(o, 'id')
				id.text = order['id']
				clover_id = ET.SubElement(o, 'clover_id')
				clover_id.text = order['clover_id']
				orderdatetime = ET.SubElement(o, 'datetime')
				orderdatetime.text = order['datetime']
				staffid = ET.SubElement(o, 'staffid')
				staffid.text = order['staffid']
				drawer = ET.SubElement(o, 'drawer')
				drawer.text = order['drawer']
				totalcache = ET.SubElement(o, 'totalcache')
				totalcache.text = order['totalcache']
				taxexempt = ET.SubElement(o, 'taxexempt')
				taxexempt.text = order['taxexempt']
				taxexemptcode = ET.SubElement(o, 'taxexemptcode')
				for amount in order['taxes']:
					tax = ET.SubElement(o, 'tax')
					tax.text = amount

				for payment in order['payments']:
					p = ET.SubElement(o, 'payment')
					paymenttype = ET.SubElement(p, 'paymenttype')
					paymenttype.text = payment['paymenttype']
					amount = ET.SubElement(p, 'amount')
					amount.text = payment['amount']

				for lineitem in order['lineitems']:
					l = ET.SubElement(o, 'lineitem')
					producttype = ET.SubElement(l, 'producttype')
					producttype.text = lineitem['producttype']
					productsize = ET.SubElement(l, 'productsize')
					productsize.text = lineitem['productsize']
					quantity = ET.SubElement(l, 'quantity')
					quantity.text = lineitem['quantity']
					nonproduct = ET.SubElement(l, 'nonproduct')
					nonproduct.text = lineitem['nonproduct']
					nontax = ET.SubElement(l, 'nontax')
					nontax.text = lineitem['nontax']
					totalsale = ET.SubElement(l, 'totalsale')
					totalsale.text = lineitem['totalsale']

					for discount in lineitem['discounts']:
						d = ET.SubElement(l, 'discount')
						amount = ET.SubElement(d, 'amount')
						amount.text = discount['amount']
						percent = ET.SubElement(d, 'percent')
						percent.text = discount['percent']
						coupon = ET.SubElement(d, 'coupon')
						coupon.text = discount['coupon']

				for discount in order['discounts']:
					d = ET.SubElement(o, 'discount')
					amount = ET.SubElement(d, 'amount')
					amount.text = discount['amount']
					percent = ET.SubElement(d, 'percent')
					percent.text = discount['percent']
					coupon = ET.SubElement(d, 'coupon')
					coupon.text = discount['coupon']

			file_parts = [file_data['outletid'], file_data['registerid']]
			existing_match = glob(os.path.join(xmldirectory, '_'.join(file_parts)+'*'))
			filename = '%s%s_%s_%s.xml' % (xmldirectory, file_data['outletid'], file_data['registerid'], str(len(existing_match)))
			# write() outputs a single line file, using _prettify() at least outputs a traditional multi-line file, which needs to be parsed back to an Element object instance
			# html method guarantees that empty child tags are closed double tags instead of closed single tag
			ET.ElementTree(ET.XML(self._prettify(root))).write(filename, encoding="utf-8", xml_declaration=True, method="html")
		except:
			self._notify_cannot_write_xml(repr(traceback.format_exc()),file_data['outletid'],file_data['salesdate']) # probably need to extend this function to include register number at some point

	# @cherrypy.expose
	# @cherrypy.tools.sa()
	# @cherrypy.tools.json_in()
	# @cherrypy.tools.json_out()
	# @cherrypy.tools.validate_hmac( keyname='clover' )
	# def salesData(self):
	# 	cherrypy.response.timeout = 360000
	# 	j = cherrypy.request.json
	# 	startday = None if 'startday' not in j else j['startday']
	# 	endday = None if 'endday' not in j else j['endday']
	# 	stores = None if 'storeids' not in j else j['storeids']
	# 	if 'yesterday' in j:
	# 		today = datetime.now()
	# 		startday = endday = isostring(today - timedelta(days=1))
	# 	if startday != None and startday != '':
	# 		day = dateutil.parser.parse(startday)
	# 		startday = datetime(day.year, day.month, day.day, 8)
	# 	if endday != None and endday != '':
	# 		day = dateutil.parser.parse(endday)
	# 		endday = datetime(day.year, day.month, day.day, 8)
	# 	delta = endday - startday
	# 	if delta.days > 31:
	# 		raise Exception('Too many days selected! Maximum of 31 days allowed.')
	# 	payment_types = self._initPaymentTypes()
	# 	timezones = self._initTimezones()
	# 	self._pull_from_clover(stores=stores, startday=startday, endday=endday, payment_types=payment_types, timezones=timezones)
	# 	return True

class Update(object):

        @cherrypy.expose
	@cherrypy.tools.sa()
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	@cherrypy.tools.validate_hmac( keyname='clover' )
	def generateStoresJSON(self):
                f = open('/tmp/stores.json','w')
                session = cherrypy.request.db.coolnet
                s = session.query(CloverInfo)\
                    .filter(Store.isdeleted == False)\
                    .filter(Store.ispos == True)\
                    .filter(Store.postypeid == 2)\
                    .all()
                jsondata = [dict(locationStoreNumber = e.store.ritasid,
                             locationInternalStoreNumber = e.store.id,
                             locationPosToken1 = dec_aes(e.merchantid,hashlib.md5(str(e.storeid)).digest()),
                             locationPosToken2 = e.apikey,
                             locationPosToken3 = '',
                             locationSystemName = e.store.posvendor.name if e.store.posvendor is not None else '',
                             locationMsa = e.store.msa.msa if e.store.msa is not None else '',
                             locationName = e.store.name,
                             locationState = e.store.state,
                             locationLatitude = e.store.latitude,
                             locationLongitude = e.store.longitude) for e in s]
                payload = json.dumps(jsondata)
                l = requests.post('http://posx.ritasfranchises.com:8091/v1/login', {"username":"mark@mdmirau.com","password":"1210Northbrook"})
                authtoken = l.json()
                r = requests.post('http://posx.ritasfranchises.com:8091/v1/config/stores/updateStores',data={'stores':payload} ,headers={'Authorization': 'Bearer '+authtoken['token']})
                with f as outfile:
                        json.dump(jsondata, outfile)

	@cherrypy.expose
	@cherrypy.tools.sa()
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	@cherrypy.tools.validate_hmac( keyname='clover' )
	def addNewCloverStore(self):
                session = cherrypy.request.db.coolnet
		j = cherrypy.request.json
		storeid = j['storeid']
		merchantid_plain = j['merchantid']
		apikey = j['apikey']
		activationtimestamp = 0 if not j['activationtimestamp'] else j['activationtimestamp']

		salt = str(storeid)
		merchantid_encrypted = enc_aes(merchantid_plain, hashlib.md5(salt).digest())

		try:
			s = session.query(CloverInfo).filter(CloverInfo.storeid == storeid).one()
			# the goal is to make sure the store doesn't exist, so return if we get a record
			return 'Cannot insert store %s, already exists in database!'%(salt)
		except:
			s = CloverInfo()
			s.storeid = storeid
			s.merchantid = merchantid_encrypted
			s.apikey = apikey
			s.activationtimestamp = datetime.utcfromtimestamp(activationtimestamp/1000)
			session.add(s)
                        p = session.query(Store).filter(Store.id == storeid).one()
                        p.ispos = True
                        p.postypeid = 2
                        session.add(p)
                        session.commit()
                        Update().generateStoresJSON()

			return 'Successfully added store %s!'%(salt)

	@cherrypy.expose
	@cherrypy.tools.sa()
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	@cherrypy.tools.validate_hmac( keyname='clover' )
        def updateActivation(self):
                session = cherrypy.request.db.coolnet
                j = cherrypy.request.json
                storeid = j['store']
                activationtimestamp = j['activationtimestamp']
                s = session.query(CloverInfo).filter(CloverInfo.storeid == storeid).one()
                s.activationtimestamp = datetime.utcfromtimestamp(activationtimestamp/1000)
                session.commit()
                return True

class Clover(object):
	#query = Query()
	#send = Send()
	#stage = Stage()
	update = Update()

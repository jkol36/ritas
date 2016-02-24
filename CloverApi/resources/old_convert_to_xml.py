from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
from xml.dom.minidom import parseString

import datetime as dt
from datetime import datetime, time, timedelta
import time
import pytz
from dateutil import tz;
from api import cloverApi

import json

import constants;

cApi = None;


'''
Gets the stores time zone and the timezone to convert to
'''
def getTimeZone(cloverAPI):
    
        elements = cloverAPI.merchant_properties(cloverAPI.merchant_id);
        timeZone = elements['timezone'];

        store_zone = pytz.timezone(timeZone);
        return store_zone;

'''
Gets the start and end time - 12AM - 11:59:59PM
'''
def getDateRangeInSeconds(storeZone):
    
    today = datetime.now(storeZone).date()
    midnight = storeZone.localize(datetime.combine(today,time(0, 0)), is_dst=None)
    startTime = (midnight - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()

    closing = storeZone.localize(datetime.combine(today, time(23, 59, 59)), is_dst=None)
    endTime = (midnight - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()

    return (startTime, endTime)


def getDateRange(storeZone):
    #Current time in store's time
    storeTime = datetime.now(storeZone);

    storeTime = storeTime.replace(day=18)

    #Start time is 6AM yesterday
    startTime = storeTime - timedelta(days=1)
    startTime = startTime.replace(hour = 6, minute = 0, second = 0);

    #End time is 12AM this morning
    endTime = storeTime.replace(hour = 0, minute = 0, second = 1);

    return (startTime, endTime);

    '''
    #Store has already closed for the day
    if storeTime.hour >= 6:

        #Start time is 6AM yesterday
        startTime = storeTime - timedelta(days=1)
        startTime = startTime.replace(hour = 6, minute = 0, second = 0);
        
        #End time is this morning
        endTime = storeTime.replace(hour = 0, minute = 1, second = 1);

    #Store closed already
    else:
        #Start time is 2 days ago
        startTime = storeTime - timedelta(days=2)
        startTime = startTime.replace(hour = 6, minute = 0, second = 0);

        #End time is yesterday
        endTime = storeTime - timedelta(days=1)
        endTime = endTime.replace(hour = 2, minute = 0, second = 0);

    return (startTime, endTime);
    '''



'''
Gets the store's time in millis and converts it to UTC time
and returns it in XML format 
'''
def getUTCTimeInXMLFormat(storeTimeInMillis, storeZone):
    storeTime = datetime.utcfromtimestamp(storeTimeInMillis / 1000.0)
    storeTime = storeTime.replace(tzinfo=storeZone);

    #HERE'S THE ISSUE
    utcZone = pytz.timezone('UTC')
    utcStoreTime = storeTime.astimezone(utcZone);

    return getTimeInXMLFormat(utcStoreTime);


'''
Returns datetime in XML string format
'''
def getTimeInXMLFormat(datetime):
    #timeFormat = "%Y-%m-%dT%H:%M:%S.%s";
    timeFormat = "%Y-%m-%dT%H:%M:%S";
    return datetime.strftime(timeFormat);

    
'''
Returns datetime in XML string format for UTC timezone
'''
def convertDateTimeToUTCXMLFormat(datetimeObject):
    utcZone = tz.gettz('UTC');
    utcTime = datetimeObject.replace(tzinfo=utcZone);
    utcTime = utcTime.astimezone(utcZone)
    return getTimeInXMLFormat(utcTime)

'''
Returns the current time in UTC timezone as XML string
'''
def currentTimeInUTCZoneAsXML():
    dateTime = datetime.utcfromtimestamp(time.time())
    return convertDateTimeToUTCXMLFormat(dateTime);

'''
Returns the difference in timezone like '-09:00'
'''
def getTimeZoneDifference(storeZone):
    difference = datetime.now(storeZone).strftime('%z')
    return difference[:3] + ":" + difference[-2:];

def getOrderTimeForXML(storeZone, orderTimeInMillis):
    orderTime = datetime.utcfromtimestamp(orderTimeInMillis / 1000.0)
    orderLocalized = storeZone.localize(orderTime)

    storeOffset = orderLocalized.strftime('%z')

    hourOffset = int(storeOffset[:3])
    isBefore = hourOffset < 0

    hourOffset = abs(hourOffset)
    minuteOffset = int(storeOffset[-2:])

    if isBefore:
        orderModifiedTime = orderTime - timedelta(hours=hourOffset, minutes=minuteOffset)
    else:
        orderModifiedTime = orderTime + timedelta(hours=hourOffset, minutes=minuteOffset)

    return getTimeInXMLFormat(orderModifiedTime)


'''
Converts the XML response to JSON
'''
def convertToXML():
    
    productInformation, sizeTypeMatching = constants.getProductsAsJSON();
    paymentTypes = constants.getPaymentTypesAsJSON();
    productAliases = constants.getProductAliasesAsJSON();

    with cloverApi(merchant_id=constants.merchant_id) as c:

        storeZone = getTimeZone(c);
        
        '''
        startTime, endTime = getDateRange(storeZone)
        startTimeInMillis = int(startTime.strftime("%s")) * 1000
        endTimeInMillis = int(endTime.strftime("%s")) * 1000
        '''

        startTime, endTime = getDateRangeInSeconds(storeZone)
        startTimeInMillis = startTime * 1000
        endTimeInMillis = endTime * 1000

        print("START TIME: " + str(startTime) + "\t" + str(startTimeInMillis))
        print("END TIME: " + str(endTime) + "\t" + str(endTimeInMillis))

        #API call to get all transactions with the expand field
        elements  = c.merchant_orders(c.merchant_id, expand={"expand": getExpandedField(), "limit": "1000", "orderBy": "clientCreatedTime"});
        orders = elements["elements"];

        root = Element('postran')

        SubElement(root, "datetime").text = currentTimeInUTCZoneAsXML();
        SubElement(root, "timezone").text = getTimeZoneDifference(storeZone);
        SubElement(root, "coolposversion").text = "CLOVER"

        outlet = SubElement(root, 'outlet')

        #Not sure about
        outletID = constants.store_id
        currency = "USD"
        registerID = 1;

        SubElement(outlet, 'id').text = str(outletID)
        SubElement(outlet, 'currency').text = currency;
        SubElement(outlet, 'registerid').text = str(registerID)

        for order in orders:

            timeInMillis = order["clientCreatedTime"];
            dateTime = getOrderTimeForXML(storeZone, timeInMillis)
            #dateTime = getUTCTimeInXMLFormat(timeInMillis, storeZone);
            
            if timeInMillis < startTimeInMillis or timeInMillis > endTimeInMillis:
                continue;

            xmlOrder = SubElement(outlet, 'order')

            #Not sure the difference between orderid and clover_id
            orderId = order["id"];
            cloverId = order["id"];
            SubElement(xmlOrder, 'id').text = orderId
            SubElement(xmlOrder, 'clover_id').text = cloverId

            dateTime = getUTCTimeInXMLFormat(timeInMillis, storeZone);
            SubElement(xmlOrder, 'datetime').text = dateTime;

            employeeId = getEmployeeId(order);
            SubElement(xmlOrder, 'staffid').text = employeeId;

            #Not sure what drawer is
            SubElement(xmlOrder, 'drawer').text = '1';

            if bool(order["taxRemoved"]):
                SubElement(xmlOrder, "taxexempt").text = '1';

            else:
                SubElement(xmlOrder, "taxexempt").text = '0';

                if 'payments' in order and 'elements' in order['payments']:
                    payments = order['payments']['elements'][0];
                    
                    if 'taxAmount' in payments:
                        taxAmount = int(payments['taxAmount'])
                        SubElement(xmlOrder, "tax").text = str(taxAmount / 100.0);

            #Not sure if this should this be empty?
            SubElement(xmlOrder, 'taxexemptcode').text = " "

            orderTotal = int(order["total"]) / 100.0

            #Not sure if this is what 'totalcache' is
            SubElement(xmlOrder, 'totalcache').text = str(orderTotal);


            #PAYMENT
            paymentXML = SubElement(xmlOrder, 'payment')

            if 'payments' in order:
                paymentsJSON = order["payments"]

                if 'elements' in paymentsJSON:
                    payments = paymentsJSON['elements'][0]
                    amount = int(payments['amount']) / 100.0;

                    tenderJSON = payments['tender'];
                    tenderLabel = tenderJSON['label']
                    paymentID = 6

                    for paymentType in paymentTypes:
                        typeName = paymentType["vchPaymentTypeName"]
                        cloverTender = paymentType["vchCloverTender"]

                        if tenderLabel in typeName or tenderLabel in cloverTender:
                            paymentID = paymentType['intPaymentTypeID']
                else:
                    amount = -1;
            else:
                amount = -1;

            SubElement(paymentXML, 'paymenttype').text = str(paymentID);
            SubElement(paymentXML, 'amount').text = str(amount);

            lineItems = order["lineItems"]["elements"];

            for lineItem in lineItems:

                lineItemXML = SubElement(xmlOrder, 'lineitem')

                if 'item' not in lineItem:
                    #print("NOT FOUND")
                    continue;

                item = lineItem["item"]
                
                itemCode = item["code"];

                if len(itemCode) > 0:
                    if itemCode in sizeTypeMatching:
                        productType = sizeTypeMatching[itemCode];

                        if itemCode in productAliases:
                            productType = productAliases[itemCode]
                    else:
                        productTye = -1;
                    productSize = itemCode;
                else:
                    productType = -1;
                    productSize = -1;

                SubElement(lineItemXML, 'producttype').text = str(productType);
                SubElement(lineItemXML, 'productsize').text = str(productSize);

                #Also not sure if this is correct
                quantity = 1;
                nonProduct = 0;
                nonTax = 0;

                SubElement(lineItemXML, 'quantity').text = str(quantity)
                SubElement(lineItemXML, 'nonproduct').text = str(nonProduct)
                SubElement(lineItemXML, 'nontax').text = str(nonTax)

                itemPrice = int(lineItem["price"]) / 100.0
                SubElement(lineItemXML, 'totalsale').text = str(itemPrice)

                if 'discounts' in lineItem:
                    discountXML = SubElement(lineItemXML, 'discount');
                    discounts = lineItem['discounts']['elements'][0];

                    if 'amount' in discounts:
                        amount = int(discounts['amount']) / 100.0;
                    else:
                        amount = 0;

                    if 'percentage' in discounts:
                        percentage = int(discounts['percentage']) / 100;
                    else:
                        percentage = 0;

                    SubElement(discountXML, 'amount').text = str(amount);
                    SubElement(discountXML, 'percent').text = str(percentage);
                    SubElement(discountXML, 'coupon').text = str(-1);

        #print(json.dumps(orders, indent=4))
        print prettify(root)


'''
Pretty prints the XML
'''
def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty = reparsed.toprettyxml(indent="        ")

    #LOOK HERE
    pretty = pretty.replace("<taxexemptcode> </taxexemptcode>", "<taxexemptcode></taxexemptcode>")
    return pretty;


'''
Returns the employee's id
'''
def getEmployeeId(order):
    if "employee" in order:
        employee = order["employee"];
        if "id" in employee:
            return employee["id"];
    return "";



'''
Returns all the expanded fields needed
'''
def getExpandedField():
    return expand(lineItems()) + expand(customers()) + expand(payments()) + expand(credits()) + expand(refunds());


'''
Returns the format for an expanded field
ex. lineItems.note,lineItems.item
'''
def expand(fieldName, fieldType = None):

    if fieldType is None:
        fieldType = fieldName[1];
        fieldName = fieldName[0];

    result = "";
    for field in fieldType:
        result += fieldName + "." + field + ",";
    return result;


'''
Returns all the line item expansion fields
'''
def lineItems():
    return ("lineItems", ["note", "item", "userData", "unitName", "itemCode", "payments", "discountAmount", "alternateName", "isRevenue", "binName", "exchangedLineItem", "taxRates", "discounts", "price", "name", "unitQty", "createdTime", "exchanged", "refunded", "id", "orderClientCreatedTime", "modifications"]);


'''
Returns all the customer item expansion fields
'''
def customers():
    return "customers", ["firstName", "lastName", "emailAddresses", "cards", "orders", "id", "phoneNumbers"];


'''
Returns all the payment item expansion fields
'''
def payments():
    return "payments", ["tender", "modifiedTime", "note", "amount", "voidReason", "lineItemPayments", "tipAmount", "cashTendered", "cardTransaction", "cashbackAmount", "employee", "refunds", "result", "clientCreatedTime", "offline", "serviceCharge", "taxRates", "createdTime", "externalPaymentId", "id", "taxAmount", "device", "amount"];


'''
Returns all the credit item expansion fields
'''
def credits():
    return "credits", ["tender", "clientCreatedTime", "amount", "taxRates", "orderRef", "cardTransaction", "createdTime", "id", "customers", "employee", "taxAmount", "device"];


'''
Returns all the refund item expansion fields
'''
def refunds():
    return "refunds", ["amount", "overrideMerchantTender", "taxableAmountRates", "employee", "lineItems", "clientCreatedTime", "serviceChargeAmount", "orderRef", "createdTime", "payment", "id", "taxAmount", "device"];


'''
Returns all the line item expansion fields
'''
def serviceCharges():
    return "serviceCharge", ["amount", "name", "id"];


'''
Returns all the discount item expansion fields
'''
def discounts():
    return "discounts", ["amount", "percentage", "name", "discount", "id"];
    

'''
Converts the JSON response to XML
'''
if __name__ == "__main__":
    convertToXML();

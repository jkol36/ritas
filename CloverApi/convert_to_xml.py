import json
import time

from datetime import datetime, timedelta
from dateutil import tz

import pytz

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
from xml.dom.minidom import parseString

from api import cloverApi
import constants


'''
Returns the datetime object in the correct format for XML
'''
def getXMLTimeFormat(timeObject):
    timeFormat = "%Y-%m-%dT%H:%M:%S"
    return timeObject.strftime(timeFormat)


'''
Returns the current UTC time in XML format
'''
def getCurrentUTCTimeInXML():
    utcTime = datetime.utcfromtimestamp(time.time())
    return getXMLTimeFormat(utcTime);


'''
Returns the difference in timezone in this format: '-09:00'
'''
def getTimeZoneDifference(storeZone):
    difference = datetime.now(storeZone).strftime('%z')
    return difference[:3] + ":" + difference[-2:];


'''
Gets the store's timezone
'''
def getStoreTimeZone(cloverAPI):
    
        elements = cloverAPI.merchant_properties(cloverAPI.merchant_id);
        timeZone = elements['timezone'];

        storeTimeZone = pytz.timezone(timeZone);
        return storeTimeZone;


'''
Computes the difference in seconds between the store's timezone and this computer's timezone
'''
def getTimeZoneDifferenceInSeconds(storeTimeZone):
    
    myTimeZone = tz.tzlocal()

    storeCurrentTime = datetime.now(storeTimeZone)
    myCurrentTime = datetime.now(myTimeZone)

    storeTimeInSeconds = time.mktime(storeCurrentTime.timetuple())
    myTimeInSeconds = time.mktime(myCurrentTime.timetuple())

    differenceInSeconds = int(storeTimeInSeconds - myTimeInSeconds)
    return differenceInSeconds


'''
Gets the start and end time of the store
The start day is yesterday at 12:00AM and the end date is yesterday at 11:59PM
Returns in milliseconds - used for querying Clover for orders
'''
def getStoreTimings(storeTimeZone):
    
    differenceInSeconds = getTimeZoneDifferenceInSeconds(storeTimeZone)

    storeTime = datetime.now(storeTimeZone)
    storeTime = storeTime - timedelta(days=1) #Yesterday

    storeStartTime = storeTime.replace(hour=0, minute=0, second=0)
    storeEndTime = storeTime.replace(hour=23, minute=59, second=59)

    storeStartTimeInSeconds = int(storeStartTime.strftime("%s")) - differenceInSeconds
    storeEndTimeInSeconds = int(storeEndTime.strftime("%s")) - differenceInSeconds

    return (storeStartTimeInSeconds * 1000, storeEndTimeInSeconds * 1000)


'''
Converts the time in seconds to the store's time
and returns it in the format for XML
'''
def getXMLFormatForStoreTime(storeTimeZone, storeTimeInSeconds):

    differenceInSeconds = getTimeZoneDifferenceInSeconds(storeTimeZone)
    convertedStoreTime = storeTimeInSeconds + differenceInSeconds

    storeTime = datetime.fromtimestamp(convertedStoreTime)
    return getXMLTimeFormat(storeTime)



'''
Converts the JSON response to XML
'''
def convertToXML():

    outletID = constants.store_id
    currency = "USD"
    
    productInformation, sizeTypeMatching = constants.getProductsAsJSON();
    paymentTypes = constants.getPaymentTypesAsJSON();
    productAliases = constants.getProductAliasesAsJSON();

    with cloverApi(merchant_id=constants.merchant_id) as c:

        storeZone = getStoreTimeZone(c);
        
        startTimeInMillis, endTimeInMillis = getStoreTimings(storeZone)
        #print("startTime: " + str(startTimeInMillis) + "\tEnd time: " + str(endTimeInMillis))

        #API call to get all transactions with the expand field
        elements  = c.merchant_orders(c.merchant_id, expand={"expand": getExpandedField(), "limit": "1000", "orderBy": "clientCreatedTime"});
        orders = elements["elements"];

        root = Element('postran')

        SubElement(root, "datetime").text = getCurrentUTCTimeInXML();
        SubElement(root, "timezone").text = getTimeZoneDifference(storeZone);
        SubElement(root, "coolposversion").text = "CLOVER"

        outlet = SubElement(root, 'outlet')

        #Not sure about
        registerID = 1;

        SubElement(outlet, 'id').text = str(outletID)
        SubElement(outlet, 'currency').text = currency;
        SubElement(outlet, 'registerid').text = str(registerID)

        for order in orders:

            timeInMillis = order["clientCreatedTime"];
            
            if timeInMillis < startTimeInMillis or timeInMillis > endTimeInMillis:
                continue;

            xmlOrder = SubElement(outlet, 'order')

            #Not sure the difference between orderid and clover_id
            orderId = order["id"];
            cloverId = order["id"];
            SubElement(xmlOrder, 'id').text = orderId
            SubElement(xmlOrder, 'clover_id').text = cloverId

            storeOrderTime = getXMLFormatForStoreTime(storeZone, int(timeInMillis / 1000))
            SubElement(xmlOrder, 'datetime').text = storeOrderTime

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

            SubElement(xmlOrder, 'taxexemptcode').text = " "

            orderTotal = int(order["total"]) / 100.0
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
                        productType = sizeTypeMatching[itemCode] #GOOD
                    else:
                        productType = -1

                    if itemCode in productAliases:
                        productSize = productAliases[itemCode]
                    else:
                        productSize = itemCode
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

                    amount = 0
                    percentage = 0
                    coupon = -1

                    if 'amount' in discounts:
                        amount = int(discounts['amount']) / 100.0;

                    if 'percentage' in discounts:
                        percentage = int(discounts['percentage']) #/100.0

                    if 'name' in discounts and 'Coupon' in discounts['name']:
                        coupon = -1 #dino_clover.py always sets coupon to -1

                    SubElement(discountXML, 'amount').text = str(amount)
                    SubElement(discountXML, 'percent').text = str(percentage)
                    SubElement(discountXML, 'coupon').text = str(coupon)

        #print(json.dumps(orders, indent=4))
        print prettify(root)


'''
Pretty print the XML
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

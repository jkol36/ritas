#Description
Accesses Rita's stores' accounts on Clover via Clover's V3 API.

The API returns the data in JSON format, which the converter changes to a custom XML format for Rita's database.


#Files and Directories

###convert_to_xml.py
Get's a stores order data (in JSON) from Clover's V3 API and converts it to XML format for Rita's database.

###constants.py
Returns the constants needed for convert_to_xml.py, ie. apiKeys, merchantIDs, productAliases, paymentTypes

###timetest.py
Merely a testing file for playing around with time conversions

###api.py, bind_api, cloverDecorators, cloverExceptions, headers.py, models.py, tests.py
Responsible for accessing Clover's V3 API 

###dino_clover.py
Old Clover API to Rita's DB converter

###resources/
Location of productAliases, merchantIDs, etc. that constants.py accesses

###Other XML
XML output/


#Run and Installation Instructions:
Coming soon, but try

    python convert_to_xml.py

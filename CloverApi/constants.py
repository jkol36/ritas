import csv
import json

#Store 1
auth_token="f4551875dcfbae15de157fb6b55bb685";
merchant_id="CNH7H10A6ACV4"
store_id=1078

#Store 2
'''
auth_token="b0627954458edaf69bbaca7f67c6c306"
merchant_id="15mf5fehcgfjc"
store_id=1097
'''

#Store 3
'''
auth_token="c007da1b-0c5c-b018-91c8-73311562a11b"
merchant_id="QZ9B6KSFXBXTY"
store_id=1044
'''


'''
Parses the payment type table and returns its values in JSON form
'''
def getPaymentTypesAsJSON():
    fileName = "resources/tblPaymentType.csv";

    reader = csv.reader(open(fileName, 'rU'), dialect=csv.excel_tab)
    rowNumber = 0;
    rowName = [];
    result = [];

    for row in reader:
        actualRow = row[0];
        elements = actualRow.split(",");

        if rowNumber == 0:
            for element in elements:
                rowName.append(element);
        else:
            counter = 0;
            resultRow = {};
            for element in elements:
                goodElement = element.replace("|", ",")
                resultRow[rowName[counter]] = goodElement;
                counter += 1;
            result.append(resultRow);
        rowNumber += 1;
    return result;


'''
Returns the product aliases
'''
def getProductAliasesAsJSON():
    fileName = "resources/productaliases.json";

    with open(fileName, 'r') as data_file:
        productAliases = json.load(data_file)
        productAliases = productAliases["productalias"]
    return productAliases;


'''
Parses the Products CSV file and returns JSON objects of their values
'''
def getProductsAsJSON():
    fileName = "resources/Products-1.csv";

    reader = csv.reader(open(fileName, 'rU'), dialect=csv.excel_tab)

    rowNumber = 0;
    rowName = [];
    result = [];
    sizeTypeMatching = {};

    for row in reader:
        goodRow = row[0];
        goodRow = goodRow.split(",");

        if rowNumber == 0:
            for column in goodRow:
                rowName.append(column)
        else:
            counter = 0;
            resultRow = {};
            for column in goodRow:
                resultRow[rowName[counter]] = column;
                counter += 1;
            result.append(resultRow);

            size = str(resultRow["Size"]);
            itemType = str(resultRow["Type"]);

            if size in sizeTypeMatching:
                print("DUPLICATE");
            else:
                sizeTypeMatching[size] = itemType;
        rowNumber += 1;

    return (result, sizeTypeMatching);


'''
Test the methods
'''
if __name__ == "__main__":
    print(json.dumps(getPaymentTypesAsJSON(), indent=4))

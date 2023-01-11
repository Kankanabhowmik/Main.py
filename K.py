import requests
import json
from datetime import datetime
from google_currency import convert
import os.path
import os

# GLOBAL VARIABLES
date = datetime.now()
url = "https://api.freecurrencyapi.com/v1/"

# STATUS API CALL
api_key = "L2VhGEg2qAHVmafQh5FWeTxeaOGwaWOGJo2iDpeD"
status_url = url + "status"
status_response = requests.get(status_url, headers={"apikey": api_key},)
status_json_data = status_response.json()
remaining_calls = status_json_data["quotas"]["month"]["remaining"]

# CURRENT PATH
cwd = os.getcwd()  # current directory
os.chdir(cwd)
data_path = cwd + "/data"

# API ALL CURRENCIES STORING FILE NAME
currencies_file_name = "allCurrencies"+str(date.month)+".json"

# ALL CURRENCIES FILE PATH
currencies_file_path = cwd+"/data/"+currencies_file_name

if (status_response.status_code == 200):

    if (os.path.exists(currencies_file_path) == False):

        # ALL CURRENCIES FROM API
        all_currencies_url = url + "currencies"
        all_currencies_response = requests.get(
            all_currencies_url, headers={"apikey": api_key}, params={"currencies": ""})

        all_curr_json_data = all_currencies_response.json()

        # CHECKING DATA FOLDER
        if (os.path.exists(data_path) == False):
            os.mkdir(data_path)

        # STORING API ALL CURRENCIES
        all_curr_json_string = json.dumps(all_curr_json_data)
        all_curr_json_file = open(currencies_file_path, "w")
        all_curr_json_file.write(all_curr_json_string)
        all_curr_json_file.close()

        all_curr_data = all_curr_json_data["data"]

    else:
        all_curr = open(currencies_file_path)
        curr_data_from_file = json.load(all_curr)
        all_curr_data = curr_data_from_file["data"]

    # PRINTING ALL CURRENCY CODES AND NAMES
    print("Currencies:\n\nCurrency Code : Currency Name")
    for item in all_curr_data:
        temp_curr_name = all_curr_data[item]["name"]
        temp_curr_code = all_curr_data[item]["code"]
        print(temp_curr_code + " : " + temp_curr_name)

    # USER INPUT
    user_base_currency = input(
        "Please enter the Currency Code from which currency you want to convert: ")
    user_convert_currency = input(
        "Please enter the Currency Code to which currency you want to convert: ")
    user_amount = int(input("Please enter the amount: "))

    # API DATA STORING FILE NAME
    searched_data_file_path = cwd+"/data/"+str(date.day)
    searched_data_file_name = user_base_currency + user_convert_currency + ".json"
    searched_data_file_full_path = searched_data_file_path+"/"+searched_data_file_name

    # CHECKING SEARCHED DATA FILE EXISTS
    if (os.path.exists(searched_data_file_path) == False):
        os.mkdir(searched_data_file_path)

    if (os.path.exists(searched_data_file_full_path) == False):

        # API CALL
        currency_url = url + "latest"
        response = requests.get(currency_url, headers={"apikey": api_key}, params={
                                "currencies": user_convert_currency, "base_currency": user_base_currency},)

        if (response.status_code == 200):

            # STORING API RESPONSE
            jsonString = json.dumps(response.json())
            jsonFile = open(searched_data_file_full_path, "w")
            jsonFile.write(jsonString)
            jsonFile.close()

            # OUTPUT DATA
            jsonData = response.json()
            output = jsonData["data"][user_convert_currency] * user_amount

            # PRINTING OUTPUT
            print("%.2f" % output)

        else:
            print(response.status_code + "Error")

    else:
        curr_val = open(searched_data_file_full_path)
        curr_val_from_file = json.load(curr_val)
        output = curr_val_from_file["data"][user_convert_currency] * user_amount

        # PRINTING OUTPUT
        print("%.2f" % output)


else:
    print("Something went wrong!")

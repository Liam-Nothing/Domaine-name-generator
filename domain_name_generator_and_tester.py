import os
import sys
import json
import base64
import grequests
from time import sleep
from datetime import datetime
from termcolor import colored
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Check if the correct number of arguments is provided
if len(sys.argv) != 4:
    print("You need three arguments: python script.py prefixes.txt words.txt top_level_domains.txt")
    sys.exit(1)

# Read input files
prefix_file = sys.argv[1]
word_file = sys.argv[2]
top_level_domain_file = sys.argv[3]

with open(prefix_file, 'r') as prefix_file, open(word_file, 'r') as word_file, open(top_level_domain_file, 'r') as tld_file:
    prefixes = prefix_file.readlines()
    words = word_file.readlines()
    top_level_domains = tld_file.readlines()

# Variables
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
url_pre = "https://www.ovh.com/engine/apiv6/order/cart/"
url_post = "/domain?domain="
urls = []
file_output = open("output_{}.log".format(dt_string), 'w')

# Functions
def log_filter(log):
    return (log["method"] == "Network.responseReceived")

# Get TOKEN
capabilities = DesiredCapabilities.CHROME
chrome_options = Options()
chrome_options.add_argument("--headless")
# capabilities["loggingPrefs"] = {"performance": "ALL"}  # Pour chromedriver < ~75
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # Pour chromedriver 75+
driver = webdriver.Chrome(desired_capabilities=capabilities, service=Service(ChromeDriverManager().install()),options=chrome_options)
driver.get("https://www.ovh.com/fr/order/webcloud/?form_id=domain_search_form#/webCloud/domain/select?selection=~()")
sleep(1)
logs_raw = driver.get_log("performance")
logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
for log in filter(log_filter, logs):
    request_id = log["params"]["requestId"]
    resp_url = log["params"]["response"]["url"]
    if (resp_url == "https://www.ovh.com/engine/apiv6/order/cart"):
        content = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
        if content['base64Encoded']:
            content = base64.b64decode(content['body'])
        else:
            content = content['body']
        print("Token get : " + json.loads(content)["cartId"])
        token = json.loads(content)["cartId"]
driver.quit()
url = url_pre + token + url_post

# Generate urls
for prefix in prefixes:
    for word in words:
        for top_level_domain in top_level_domains:
            domain_name = "{}{}{}".format(prefix.strip(), word.strip(), top_level_domain.strip())
            urls.append(url + domain_name)

# Requests urls
requests = (grequests.get(u) for u in urls)
responses = grequests.map(requests)
json = [response.json() for response in responses]

# Writing
print("\n====== Domains Name Generator ======")
for idx,item in enumerate(json):
    domaine = urls[idx].split('=')[-1]
    if isinstance(item, list):
        if not len(item) == 0:
            if 'action' in item[0]:
                if (item[0]["action"] == "create") and (item[0]["pricingMode"] == "create-default"):
                    print(colored("[AVAILABLE] ", "green") + domaine + colored(" " + item[0]["prices"][1]["price"]["text"], "magenta"))
                    file_output.writelines(domaine + item[0]["prices"][1]["price"]["text"] + "\n")
                elif item[0]["pricingMode"] == "transfer-default" :
                    print(colored("[TRANSFER] ", "red") + domaine + colored(" " + item[0]["prices"][0]["price"]["text"], "cyan"))
                else :
                    print(colored("[TRADE] ", "yellow") + domaine + colored(" " + item[0]["prices"][0]["price"]["text"], "cyan"))
        else:
            print(colored("[NO] ", "red") + domaine)
    else:
        print(colored("[?] ", "blue") + domaine)
file_output.close()

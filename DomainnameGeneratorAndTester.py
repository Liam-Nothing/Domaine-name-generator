import grequests
import pprint
from datetime import datetime
from termcolor import colored
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import json
import base64
from selenium.webdriver.chrome.options import Options

now = datetime.now()
dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
url_pre = "https://www.ovh.com/engine/apiv6/order/cart/"
url_post = "/domain?domain="

# Get TOKEN
capabilities = DesiredCapabilities.CHROME
chrome_options = Options()
chrome_options.add_argument("--headless")
# capabilities["loggingPrefs"] = {"performance": "ALL"}  # Pour chromedriver < ~75
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # Pour chromedriver 75+
driver = webdriver.Chrome(desired_capabilities=capabilities, executable_path="chromedriver.exe",options=chrome_options)
driver.get("https://www.ovh.com/fr/order/webcloud/?form_id=domain_search_form#/webCloud/domain/select?selection=~()")
sleep(1)
logs_raw = driver.get_log("performance")
logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

def log_filter(log):
	return (log["method"] == "Network.responseReceived")

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

file_pref = open('pref.txt', 'r')
lines_pref = file_pref.readlines()
file_word = open('word.txt', 'r')
lines_word = file_word.readlines()
file_suf = open('suf.txt', 'r')
lines_suf = file_suf.readlines()

urls = []

# Generate urls
for line_suf in lines_suf:
	for line_pref in lines_pref:
		for line_word in lines_word:
			domainName = ("{}{}{}".format(line_pref.strip(),line_word.strip(), line_suf.strip()))
			urls.append(url + domainName) 
requests = (grequests.get(u) for u in urls)
responses = grequests.map(requests)

json = [response.json() for response in responses]
file_out = open("output_{}.txt".format(dt_string), 'w')

for idx,item in enumerate(json):
	domaine = urls[idx].split('=')[-1]
	if isinstance(item, list) and len(item)>0:
		if 'action' in item[0]:
			if (item[0]["action"] == "create") and (item[0]["pricingMode"] == "default"):
				print(colored("[AVAILABLE] ", "green") + domaine)
				file_out.writelines(domaine + "\n")
			else:
				print(colored("[AVAILABLE] ", "yellow") + domaine)
		else:
			print(colored("[NO] ", "blue") + domaine)
	else:
		print(colored("[NO] ", "red") + domaine)

file_out.close()
import socket
import whois
import sys
from datetime import datetime

now = datetime.now()

dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")	

file_pref = open('pref.txt', 'r') 
lines_pref = file_pref.readlines()
count_pref = 0

file_word = open('word.txt', 'r') 
lines_word = file_word.readlines()
count_word = 0

file_suf = open('suf.txt', 'r') 
lines_suf = file_suf.readlines()
count_suf = 0

count_total = 0

def startProgress(title):
    global progress_x
    sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    sys.stdout.flush()
    progress_x = 0

def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("#" * (x - progress_x))
    sys.stdout.flush()
    progress_x = x

def endProgress():
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()

for line_suf in lines_suf: 
	for line_pref in lines_pref: 
		for line_word in lines_word:
			count_total += 1
# print(count_total)

startProgress("Find Domain")
file_out = open("output_{}.txt".format(dt_string), 'w')
for line_suf in lines_suf: 
	for line_pref in lines_pref: 
		for line_word in lines_word: 
			domainName = ("{}{}{}".format(line_pref.strip(), line_word.strip(), line_suf.strip()))
			# file_out.writelines(domainName)
			# file_out.writelines("\n")
			try:
				x = (socket.gethostbyname(domainName)," = ",domainName)
			except socket.error:
				try:
					w = whois.whois(domainName).expiration_date
				except:
					# print(domainName)
					file_out.writelines(domainName)
					file_out.writelines("\n")
			count_word += 1
			var_progress = int(count_word/count_total*100)
			progress(var_progress)
file_out.close()
endProgress()
# print("\nEnd\n",count_word)
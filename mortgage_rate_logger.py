# Title:		Mortgage Rate Tracker
# Version:		1.0
# Author: 		Justin Barth
# Created:		03/17/2020
# Purpose:		To track rate changes on mortgage options and email if rates drop below a set threshold
# Dependencies:	Must have the chromedriver.exe in the same directory as this program
#				Must have Google Chrome installed
# Arguments:	None
# Known Issues/Limitations: None
#
# Change Log:
#	1.0: initial release


from selenium import webdriver					# Used to open the browser
import os.path									# Used to check for file exists
import time										# Timestamp files
import os										# Get current directory
import sys										# Stop program

NFCU_URL	= 'https://www.navyfederal.org/loans-cards/mortgage/refinancing/'
RATES_CSV	= 'NFCU_VA_IRRRL_Rates.csv'
TARGET_RATE	= 2.5

# FUNCTIONS
def print_and_log(msg, lvl=0, mode="a+", filename=""):
	msg = msg.rjust(lvl*3 + len(msg))
	print(msg)
	if filename == "":
		filename = logfile
	file = open(filename, mode)
	file.write(msg + "\n")
	file.close()

def email_rate(rate, apr):
	print_and_log('rate (' + str(rate) + ') < TARGET_RATE (' + str(TARGET_RATE) + '), sending email notification...',1)
	
	cwd = os.getcwd()
	email_template_file = cwd + '\\email_template.txt'
	email_parameters = 'template="'	+ email_template_file + '" subject="Mortgage Rate Tracker - Act Fast"'
	email_parameters += ' template.rate=' + str(rate) + '%'
	email_parameters += ' template.apr=' + apr

	os.chdir("..\\send_mail")
	os.system("py .\send_mail.py " + email_parameters)
	os.chdir(cwd)
	print_and_log("Email Complete",1)


# Setup logging
start_time = time.strftime("%Y-%m-%d_%H:%M")
logfile = "logfile.txt"
print("logfile = " + logfile)

# START
print('Mortgage Rate Checker')
print_and_log('Start Time: ' + start_time)

# Browser Setup
try:
	options = webdriver.ChromeOptions()
	options.add_argument('log-level=3')					# Only show Fatal Error
	#browser = webdriver.Chrome(chrome_options=options)
	browser = webdriver.Chrome(options=options)
except:
	print_and_log("Error: Must have Google Chrome installed (hint: run ChromeSetup.exe)",1)
	sys.exit(ERROR_NO_CHROME)

print_and_log("Accessing website: " + NFCU_URL,1)
browser.get(NFCU_URL)
time.sleep(2)

element = browser.find_elements_by_xpath('//*[@id="refinance-options"]/div/ul/li[2]/div[2]/div[1]/p')
rate = element[0].text
element = browser.find_elements_by_xpath('//*[@id="refinance-options"]/div/ul/li[2]/div[2]/div[2]/p')
apr = element[0].text

print_and_log('Rate:' + rate + ' APR: ' + apr,1)

# Print header if the file does not exists
if not os.path.exists(RATES_CSV):
	file = open(RATES_CSV, "w")
	file.write(RATES_CSV[:-4] + '\n')
	file.write('Time, Date, Rate, APR\n')
	file.close()

file = open(RATES_CSV, "a+")
file.write(time.strftime("%Y-%m-%d") + ',' + time.strftime("%H:%M") + ',' + rate + ',' + apr + '\n')
file.close()

# Email if rate < TARGET_RATE
rate = float(rate[:-1])
if (rate < TARGET_RATE):
	email_rate(rate, apr)
else:
	print_and_log('rate (' + str(rate) + ') >= TARGET_RATE (' + str(TARGET_RATE) + ') no notification sent',1)


browser.quit()

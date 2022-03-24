from selenium import webdriver
import time
import csv
#from urlListClass import urlList

# Vars
addressList = []
phoneList = []
currentUrl = []
PATH = './chromedriver.exe'
urlList = ['https://www.menu.com.do/#!/n/100_Montaditos','https://www.menu.com.do/#!/n/30_Sinco', 'https://www.menu.com.do/#!/n/Agualaboca']

# Loop url list defined in urlistclass.py
for url in urlList:
    # Save the current url on a list, to follow up on the order with the address and phone lists.
    currentUrl.append(url)
    # Instantiate Selenium driver located in path
    driver = webdriver.Chrome(PATH)
    # GET url using driver
    driver.get(url)
    # Wait for 7 seconds for the url to execute all js scripts
    time.sleep(7)
    # Copy url source code to var
    html = driver.page_source
    addressRaw = ''
    phoneRaw = ''
    # Find desired code chunk
    if 'streetAddress' in html:
        addressRaw = html[html.find('streetAddress'):html.find('streetAddress')+200]
        startIndex = addressRaw.find('ng-binding')
        endIndex = addressRaw.find('</span></div>')
        addressList.append(addressRaw[startIndex + 12:endIndex])
    # If code chunk is not found, append an N/A to list
    else:
        addressList.append('N/A')
    # Find desired code chunk
    if '(809)' in html or '(829)' in html or '(849)' in html:
        phoneRaw = html[html.find('9)')-3:html.find('9)')+11]
        phoneList.append(phoneRaw)
    # If code chunk is not found, append an N/A to list
    else:
        phoneList.append('N/A')
    # Close the current Selenium browser window
    driver.close()

# Write data on CSV file.
with open('data.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    for i in range(len(currentUrl)):
        writer.writerow([currentUrl[i], addressList[i], phoneList[i]])
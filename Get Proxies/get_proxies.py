# This scripts fetches free proxies of the internt.
# You can import or copy paste this into your code. 

import requests 
from bs4 import BeautifulSoup as bs
import os
import csv
import datetime
import time

def fetch_proxies():
	proxies = []
	PROXY_URLS = ["https://free-proxy-list.net/"]
	for url in PROXY_URLS:
		success = False
		while not success:
			try:
				page = requests.get(url)
				soup = bs(page.content, "html.parser")
				for row in soup.findAll('table')[0].tbody.findAll('tr'):
					columns = row.findAll('td')
					ip = columns[0].contents[0]
					#print (ip)
					port = columns[1].contents[0]
					#print (port)
					protocol = columns[5].contents[0].lower()
					protocol1 = columns[6].contents[0].lower()

					#print (protocol)
					proxies.append((ip, port, protocol,protocol1))
				success = True
				if(os.path.exists('../record.csv') == False):
					with open('../record.csv','w') as csv_file:
						csv_writer = csv.writer(csv_file,delimiter=',')
						csv_writer.writerow(["Source","Time"])
				with open('../record.csv','a') as csv_file:
					csv_writer = csv.writer(csv_file,delimiter=',')
					csv_writer.writerow(["BR",str(datetime.datetime.now())])

			except Exception as ex:
				print(ex)
				print('Cannot get proxy')
				success = False
				exit()
	filtered_proxies = [p for p in proxies if (p[2] in "yes") or (p[3] in "yes") ]
	return filtered_proxies

list_proxies = fetch_proxies()
print(list_proxies)

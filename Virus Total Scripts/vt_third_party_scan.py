import requests
import os
import sys
import json
from time import sleep
import requests


apiKeys = []

def appendHashToFile(hash):
    with open(HASH_FILE,'a+') as f:
        f.write(str(hash)+'\n')

def sendDomaim(domain,apikey):


    url = 'https://www.virustotal.com/vtapi/v2/url/report'

    params = {'apikey': apikey, 'resource':domain}

    response = requests.get(url, params=params)
    res = response.json()
    scan = res["scans"][0]
    return scan


def main():
    global apiKeys
    apiKeys = open("apiKeys.txt",'r').read().split('\n')
    apiKeys = list(filter(lambda x: not x=="",apiKeys)) 
    input("Press Enter to continue...")

    domain_list = ["nbcume.sc.omtrdc.net", "settings.crashlytics.com", "connect.tapjoy.com"]

    api_count = len(apiKeys)
    count = 0
    for x in domain_list:
        res = sendDomaim(x, apiKeys[count])
        print(res)
        count = (count + 1) % api_count
    

if __name__ == "__main__":
    main()
    
    
    
    




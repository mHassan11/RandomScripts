import requests
import os
import sys
import json
DEST_FOLDER = "FinalReports"



def askOneReport(resource,apikey):
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': apikey, 'resource': resource}
    response = requests.get(url, params=params)
    try:
        ret = response.json()
        return ret
    except:
        print(response)
        return "Error"

def askAllReports(foldername,resources,apikeys):
    if not os.path.isdir(DEST_FOLDER):
        os.mkdir(DEST_FOLDER)
    tempFileName = 0 #REMOVE
    apiIndex = 0
    for resource in resources:
        report = askOneReport(resource,apikeys[apiIndex])
        with open(os.path.join(DEST_FOLDER,str(tempFileName)+'.json'), 'w') as f:
            json.dump(report, f, ensure_ascii=False, indent=4)
        apiIndex = apiIndex + 1
        tempFileName = tempFileName + 1 #REMOVE
        if(apiIndex >= len(apikeys)):
            apiIndex = 0
        print(tempFileName)
    print("All Done")

def collector(foldername):
    with open('apiKeys.txt','r') as f:
        apikeys = f.read().split('\n')
    with open('hashes.txt','r') as f:
        hashes = f.read().split('\n')
    apikeys = list(filter(lambda x: not x=="",apikeys))
    hashes = list(filter(lambda x: not x=="",hashes))
    askAllReports(foldername,hashes,apikeys)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        collector(sys.argv[1])
    else:
        collector('uploadreports')
            
            

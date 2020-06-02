import requests
import os
import sys
import json
from time import sleep

HASH_FILE = 'hashes.txt'
SEND_REPORT_FOLDER = "SendReportFolder"
INITIAL_FOLDER = 'filestoscan'
apiKeys = []
def appendHashToFile(hash):
    with open(HASH_FILE,'a+') as f:
        f.write(str(hash)+'\n')
def sendOneFile(filename,apikey):
   
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    print('FileName:',filename)
    params = {'apikey': apikey}
    files = {'file': (filename, open(filename, 'rb'))}
    
    try:
    	response = requests.post(url, files=files, params=params)
    except:
        print("Exception raised")
        return("Call again")
    print(response.json()['sha256'])
    return response.json()

def sendAllFiles(foldername):
    destination_folder = os.path.join(SEND_REPORT_FOLDER,foldername)
    initial_folder = os.path.join(INITIAL_FOLDER,foldername)
    filenames = os.listdir(initial_folder)
    if not os.path.isdir(destination_folder):
        os.mkdir(destination_folder)
    apiIndex = 0
    for filename in filenames:
        if not filename == 'requests.json':
            report = sendOneFile(os.path.join(initial_folder,filename),apiKeys[apiIndex])
            val=0
            if(report=="call again" and val<3):
                report = sendOneFile(os.path.join(initial_folder,filename),apiKeys[apiIndex])
                val=val+1
            else:
                 if(report!="call again" and val<3):
                       with open(os.path.join(destination_folder,filename+'.json'), 'w', encoding='utf-8') as f:
                            json.dump(report, f, ensure_ascii=False, indent=4)
                       #appendHashToFile(report['sha256'])
                       apiIndex = apiIndex + 1
                       if(apiIndex >= len(apiKeys)):
                           apiIndex = 0
                
                
    print("All Done")


def main():
    global apiKeys
    apiKeys = open("apiKeys.txt",'r').read().split('\n')
    apiKeys = list(filter(lambda x: not x=="",apiKeys)) 
    dir_list = os.listdir(INITIAL_FOLDER)
    if not os.path.isdir(SEND_REPORT_FOLDER):
        os.mkdir(SEND_REPORT_FOLDER)
    for entry in dir_list:
        sendAllFiles(entry)
    input("Press Enter to continue...")
    

if __name__ == "__main__":
    # if len(sys.argv) == 2:
    #     collector(sys.argv[1])
    # else:
    #     collector('filestoscan')
    main()
    
    
    
    




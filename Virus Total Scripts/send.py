import requests
import os
import sys
import json

SOURCE="SendReportFolder"
SINK="FINAL_Reports"

def askOneReport(resource,apikey):
     url = 'https://www.virustotal.com/vtapi/v2/file/report'
     params = {'apikey': apikey, 'resource': resource}
     try:
              response = requests.get(url, params=params)
              try:
                 ret = response.json()
                 return ret
              except:
                 print(response)
                 return "Error"
     except:
              print("Exception raised")
              return("Call again")

def sendAllFiles(foldername,apiKeys):
    destination_folder = os.path.join(SINK,foldername)
    initial_folder = os.path.join(SOURCE,foldername)
    filenames = os.listdir(initial_folder)
    apiIndex = 0
    if not os.path.isdir(destination_folder):
        os.mkdir(destination_folder)
    for filename in filenames:
            with open(os.path.join(initial_folder,filename), 'r') as f:
                 distros_dict = json.load(f)
            resource=distros_dict["sha256"]
            print(resource)
            name=(filename.split("."))
            name=name[0]
            report = askOneReport(resource,apiKeys[apiIndex])
            val=0
            if(report=="call again" and val<3):
                     report = askOneReport(resource,apiKeys[apiIndex])
                     val=val+1
            else:
                if(report!="call again" and val<3):
                      with open(os.path.join(destination_folder,name+'.json'), 'w', encoding='utf-8') as f:
                              json.dump(report, f, ensure_ascii=False, indent=4)
                      apiIndex = apiIndex + 1
                      if(apiIndex >= len(apiKeys)):
                             apiIndex = 0

def main():
    dir_list = os.listdir(SOURCE)
    with open('apiKeys.txt','r') as f:
        apikeys = f.read().split('\n')
    if not os.path.isdir(SINK):
        os.mkdir(SINK)
    for entry in dir_list:
        sendAllFiles(entry,apikeys)
    input("Press Enter to continue...")


if __name__ == "__main__":
    # if len(sys.argv) == 2:
    #     collector(sys.argv[1])
    # else:
    #     collector('filestoscan')
    main()

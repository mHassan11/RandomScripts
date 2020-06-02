import os
import json
dirList = os.listdir('FinalReports')
detected = []
for sourceFile in dirList:
    with open(os.path.join('FinalReports',sourceFile)) as f:
        data = json.load(f)
    try:
        for scan in data['scans']:
            if data['scans'][scan]['detected']:
                detected.append(data)
                print("Found",sourceFile)
    except:
        #print('Error',sourceFile)
        pass
with open('Detected.txt','w+') as f:
    f.write(json.dumps(detected,indent=4, sort_keys=True))
            

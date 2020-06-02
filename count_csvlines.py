#read all lines of csv files in 'dir' directory

import os
import glob

path = "./dir" 
os.chdir(path)
result = [i for i in glob.glob('*.{}'.format("csv"))]

count_tweet = 0
for i in result:
   with open(i, 'r', encoding="latin-1") as csvfile:
    count_tweet = count_tweet + len(csvfile.readlines()) - 1
    # print(i, ": ", str(len(csvfile.readlines()) - 1))

print("Total Files " + str(len(result)))
print("Total Lines " + str(count_tweet))
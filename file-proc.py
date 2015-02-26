#!/usr/bin/python

import time 
import pprint
import os.path

timestamp = time.time()
copyTmp = 'cp crunchbase.csv crunchbase.csv-' + str(timestamp)
stripHeaderCmd = 'tail -n +2 crunchbase.csv > crunchbase.csv.old'
mergeCmd = 'cat crunchbase.csv.old crunchbase.csv.1 crunchbase.csv.2 crunchbase.csv.3 > merged.csv'
cleanCmd = 'sort -t , --key=1,5 -r merged.csv | sort -t , --key=1,1 --unique | sort -t , -k 5 -r > clean.csv'
addHeaderCmd = 'echo "Name,Path,Type,Created Date,Updated Date,Role Company,Secondary role for profit,Short description,Permalink,Primary role,Is closed,Closed on trust code,Website,Founded on,Founded on trust code,Closed on,Num employees range,Total funding usd,Number of investments,Founders,Local url,Remote url" > crunchbase.csv'
moveCmd = 'cat clean.csv >> crunchbase.csv' 
removeCmd = 'rm merged.csv crunchbase.csv.new crunchbase.csv.old clean.csv' 
os.system(copyTmp)
os.system(stripHeaderCmd)
os.system(mergeCmd)
os.system(cleanCmd)
os.system(addHeaderCmd)
os.system(moveCmd)
os.system(removeCmd)
print 'file processing in ' + str(time.time() - timestamp) + ' seconds.'
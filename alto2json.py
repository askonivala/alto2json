#! /usr/bin/python
#
# Convert ALTO XML to JSON by Asko Nivala (aeniva@utu.fi)
# 2. March 2016

import os
import sys
import xmltodict
import json
import io
from collections import OrderedDict

# Setting the current path as the root directory 
rootDir = sys.path[0]

for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: %s' % dirName)
    for fname in fileList:
        if fname.endswith('xml'):
            fullpath = os.path.join(rootDir, dirName, fname)
            print fullpath
            with open(fullpath,'r') as fd:
                doc = xmltodict.parse(fd.read())
            fd.close()
            sarja = fname[0:9]
            # Check for empty class.
            try:
                data = {
                    'id' : fname,
                    'series' : sarja,
                    'title' : doc['pageOCRData']['metadata']['title'],
                    'date' : doc['pageOCRData']['metadata']['published']['#text'],
                    'lang' : doc['pageOCRData']['metadata']['language'],
                    'URL' : doc['pageOCRData']['metadata']['imageURL'],
                    'text' : doc['pageOCRData']['content']['text']['#text']
                }
            except KeyError:
                data = {
                    'id' : fname,
                    'series' : sarja,
                    'title' : doc['pageOCRData']['metadata']['title'],
                    'date' : doc['pageOCRData']['metadata']['published']['#text'],
                    'lang' : doc['pageOCRData']['metadata']['language'],
                    'URL' : doc['pageOCRData']['metadata']['imageURL'],
                    'text' : ''
                }

            with open('./data.json','a') as outfile:
                json.dump(data, outfile, sort_keys=False)
                outfile.write('\n')
            outfile.close()
            data = {}
        else:
            print('Skipping file...')
import sys
import requests
import os
import json
from xml.dom.minidom import parseString

calais_url = 'https://api.thomsonreuters.com/permid/calais'

def main():
    try:
        if len(sys.argv) < 3:
            print '2 params are required: 1.input file full path, 2.access token'
            sys.exit(-1)
        else:
            input_file = sys.argv[1]
            access_token = sys.argv[2]

            if not os.path.exists(input_file):
                print 'The file [%s] does not exist' % input_file
                return

        headers = {'X-AG-Access-Token' : access_token, 'Content-Type' : 'text/raw', 'outputformat' : 'application/json'}
        sendFiles(input_file, headers)
    except Exception ,e:
        print 'Error in connect ' , e

def sendFiles(files, headers):
    is_file = os.path.isfile(files)
    if is_file == True:
        sendFile(files, headers)
    else:
        for file_name in os.listdir(files):
            if os.path.isfile(file_name):
                sendFile(file_name, headers)
            else:
                sendFiles(file_name, headers)

def sendFile(file_name, headers):
    files = {'file': open(file_name, 'rb')}
    response = requests.post(calais_url, files=files, headers=headers, timeout=80)
    content = response.text
    #print 'Results received: %s' % content
    if response.status_code == 200:
	oc_response_json = json.loads(content);
	#print findall(oc_response_json, 'socialTag');
	findall(oc_response_json, 'socialTag');

def findall(v, k):
  if type(v) == type({}):
     for k1 in v:
         if k1 == k:
	    #result.append(v['name'].encode("utf-8"));
            print v['name'] + ',';
            #print v[k1]
         findall(v[k1], k)

if __name__ == "__main__":
   main()

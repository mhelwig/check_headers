#!/usr/bin/python

import urllib2
import re

'''
check_headers.py

Checking http headers for given values

Usage: python check_headers.py

author: Michael Helwig (@c0dmtr1x)
license: LGPLv3

Adjust config settings before use

'''

##########
# config #
##########

#user-agent
useragent = "Mozilla/5.0"

#protocol
protocols = ["https","http"]

# list your domains
domains = [
     "www.google.com", 
     "www.google.de", 
     "www.google.fr", 
     "www.google.it",
]


# expected headers
expected = {
    # check for multiple regex matches
    "set-cookie" : [
        { 
          "contains":["HttpOnly"],
          "required": True
        },
        {
            "contains":["Secure"],
            "required": {
                "protocol":["https"]
            }
        
        }
    ],

    "strict-transport-security": {
          "contains":"max-age=15552000",
          "required":{
              "protocol":["https"]
          }
    },
    "x-xss-protection":{
         "value":"1; mode=block",
          "required":True
    },
    "x-content-type-options":{
          "value":"nosniff",
          "required":True
    },
    "x-frame-options":{
        "value":"SAMEORIGIN",
        "required":True
    },
    "dummy":{
        "contains":"1",
        "required":False
     }
}

#timeout for url requests
timeout = 5

#follow redirects or not
follow_redirects = True

#################
# header check  #
#################

class HeaderRedirectHandler(urllib2.HTTPRedirectHandler):
    global follow_redirects
    def http_error_301(self, req, fp, code, msg, headers):
        if not follow_redirects:
            print " [ERROR] Not following redirect to " + headers["location"]
            return False
        else:
            print " [INFO] Following redirect to " + headers["location"]
        result = urllib2.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)
        result.status = code
        return result

    def http_error_302(self, req, fp, code, msg, headers):
        if not follow_redirects:
            print " [ERROR] Not following redirect to " + headers["location"]
            return False
        else: 
            print " [INFO] Following redirect to " + headers["location"]
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)              
        result.status = code  
        return result

def check_header(info,key,expected_entry,protocol):
    if "value" in expected_entry.keys() and expected_entry["value"] == info[key]:
        print " [OK] " + key + ": " + info[key]
    elif "value" in expected_entry.keys() and (expected_entry["required"] == True or (isinstance(expected_entry["required"],dict) and "protocol" in expected_entry["required"] and protocol in expected_entry["required"]["protocol"])):
        print " [ERROR] Unexpected " + key + ": " + info[key]
    if "contains" in expected_entry.keys():
        for contains_entry in expected_entry["contains"]:
            if re.match(info[key],contains_entry):
	        print " [OK] " + key +" matches " + contains_entry
            elif expected_entry["required"] == True or isinstance(expected_entry["required"],dict) and "protocol" in expected_entry["required"] and protocol in expected_entry["required"]["protocol"]:
	        print " [ERROR] " + key + " does not match " + contains_entry

for domain in domains:
    for protocol in protocols:
	url = protocol + "://" + domain
	print "\n[URL] "+  url
	try:
	    opener = urllib2.build_opener(HeaderRedirectHandler)
	    opener.addheaders = [('User-Agent', useragent)]
	    response = opener.open(url,timeout=timeout)
	    info = response.info()
	    for key in expected.keys():
		 if key in info:
                     if isinstance(expected[key],dict):
                         check_header(info,key,expected.get(key),protocol)
                     elif isinstance(expected[key],list):
                         for entry in expected.get(key):
                             check_header(info,key,entry,protocol)
		 else:
		     if expected.get(key)["required"]:
			 print " [ERROR] Missing " + key

	except IOError, e:
	    if hasattr(e,'code'):
		print " [ERROR] Host responded with status " + str(e.code)
	    else:
		print " [ERROR] Could not retrieve url. Skipped."


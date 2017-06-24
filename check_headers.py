#!/usr/bin/python

import urllib2

'''
check_headers.py

Checking http headers for given values

Usage: python check_headers.py

author: Michael Helwig (@c0dmtr1x)
license: Use at will (None)

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
    "strict-transport-security":{
          "value":"max-age=15552000",
          "required":True
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
        "value":"1",
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


for domain in domains:
    for protocol in protocols:
	url = protocol + "://" + domain
	print "\n[URL] "+  url
	try:
	    opener = urllib2.build_opener(HeaderRedirectHandler)
	    opener.addheaders = [('User-Agent', useragent)]
	    response = opener.open(url,timeout=timeout)
	    info = response.info()
	    for i in expected.keys():
		 if i in info:
		     if expected.get(i)["value"] == info[i]:
			 print " [OK] " + i + ": " + info[i]
		     elif expected.get(i)["required"]:
			 print " [ERROR] Unexpected " + i + ": " + info[i]
		 else:
		     if expected.get(i)["required"]:
			 print " [ERROR] Missing " + i

	except IOError, e:
	    if hasattr(e,'code'):
		print " [ERROR] Host responded with status " + str(e.code)
	    else:
		print " [ERROR] Could not retrieve url. Skipped."


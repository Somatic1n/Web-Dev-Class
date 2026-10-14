#!/usr/bin/env python3


import os
import sys
import urllib.parse

# Determine if request is POST or GET
request_method = os.environ.get('REQUEST_METHOD', 'GET').upper()

if request_method == "POST":
    content_length = int(os.environ.get('CONTENT_LENGTH', 0) or 0)
    post_data = sys.stdin.read(content_length)
    qs_values = urllib.parse.parse_qs(post_data, keep_blank_values=True)
else:
    query_string = os.environ.get('QUERY_STRING', '')
    qs_values = urllib.parse.parse_qs(query_string, keep_blank_values=True)

# Retrieve the values sent from the client
fullname = qs_values['name'][0] 
email = qs_values['email'][0]
subject = qs_values['subject'][0]
message = qs_values['message'][0]


#**********Output HTML**********

print ("Content-type:text/html\r\n\r\n") #Must have this header
print ("<!DOCTYPE html>")
print ("<html>")
print ("<head>")
print ("<title>Hello Somebody</title>")
print ("</head>")
print ("<body>")
print ("<h2>Hello, %s!</h2>" % (fullname))
print ("<h2>Email: %s!</h2>" % (email))
print ("<h2>Subject: %s!</h2>" % (subject))
print ("<h2>Message: %s!</h2>" % (message))
print ("</body>")
print ("</html>")



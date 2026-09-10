#! C:\Python313\python.exe

import os
import sys
import urllib.parse
from http import cookies

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

fname = qs_values['fname'][0] 
lname = qs_values['lname'][0]

#**********Create a cookie object to use for both the session and the Cookie

cookie = cookies.SimpleCookie()

#********** Create a Session File and Store the Session Variables**********

# Check if the session cookie exists, if so read the value
if 'HTTP_COOKIE' in os.environ:
    cookie.load(os.environ['HTTP_COOKIE'])
    if 'session_id' in cookie:
        session_id = cookie['session_id'].value
    else:
        session_id = None
else:
    session_id = None

# If no session ID, create a new one
if not session_id:
    import uuid
    session_id = str(uuid.uuid4())
    cookie['session_id'] = session_id

session_file_path = f'\\tmp\\session_{session_id}.txt'  #Must be a file with WRITE access
with open(session_file_path, 'w') as session_file:
    if fname:
        session_file.write(f'fname={fname}\n')
    if lname:
        session_file.write(f'lname={lname}\n')

#**********Create and Print the Cookie Before (Important!) the HTML Header**********

cookie['FullName'] = fname + " " + lname
print(cookie)

#**********Output the HTML**********

print ("Content-type:text/html\r\n\r\n") #HTML Header
print ("<!DOCTYPE html>")
print ("<html>")
print ("<head>")
print ("<title>Session Variables</title>")
print ("</head>")
print ("<body>")
print ("<h2>Session Variables Stored</h2>")
if fname:
    print (f"<p>First Name: {fname}</p>")
if lname:
    print (f"<p>Last Name: {lname}</p>")
print (f"<script>localStorage.setItem('LastName', '{lname}');</script>");  #Send back JavaScript to save to local storage
print ("</body>")
print ("</html>")



#! C:\Python313\python.exe

import os
import sys
import urllib.parse
import mysql.connector 
from mysql.connector import errorcode
import bcrypt
import warnings
import json
warnings.filterwarnings("ignore", category=DeprecationWarning)


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

q = qs_values['q'][0] 

#**********Connect to Database**********
HOST = "localhost"
USER = "DemoUser"
PASSWORD = "DemoPassword!"
DATABASE = "DemoDB"
AUTHPLUGIN = "mysql_native_password"

DBResponse = ""
try:
  mydb = mysql.connector.connect(host=HOST,user=USER,password=PASSWORD, database=DATABASE, auth_plugin= AUTHPLUGIN)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    DBResponse = "Something is wrong with the user name or password"
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    DBResponse = "Database does not exist"
  else:
    DBResponse = err
  
mycursor = mydb.cursor()

#**********Retrieve a list of possible Names**********
sql = "SELECT UserName FROM user WHERE UserName LIKE %s"
val = (q + '%',)  
mycursor.execute(sql, val)
myresult = mycursor.fetchall()

hint = "no suggestion"

for x in myresult:
     if hint == "no suggestion":
           hint = x[0]
     else:
           hint = hint + " , " + x[0]
           
print("Content-Type: application/json\n")
print(json.dumps({"suggestion": hint}))
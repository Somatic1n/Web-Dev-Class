#! C:\Python313\python.exe

import os
import sys
import urllib.parse
import mysql.connector 
from mysql.connector import errorcode
import bcrypt
from  DBConnection import HOST, USER, PASSWORD, DATABASE, AUTHPLUGIN

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

username = qs_values['username'][0] 
password = qs_values['password'][0]
email = qs_values['email'][0]

#**********Hash the password**********

password_bytes = password.encode('utf-8')
hashedpassword = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

#**********Connect to Database**********

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

#**********Execute the SQL Statement to Insert the Record **********

sql = "INSERT INTO user (UserName, Email, Password) VALUES ( %s, %s, %s)"
val = (username, email, hashedpassword)
try:
  mycursor.execute(sql, val)
  mydb.commit()
  DBResponse = "User added successfully!"
except mysql.connector.Error as err:
  DBResponse = "Error on insert: {}".format(err)
mydb.close()

#**********Output HTML**********

print ("Content-type:text/html\r\n\r\n") 
print ("<!DOCTYPE html>")
print ("<head>")
print ("<title>Python Crud Create</title>")
print ("</head>")
print ("<body>")
print (DBResponse)
print ("<br><br><a href='read.py'>View List</a>")
print ("<br><br><a href='index.html'>Crud Home</a>")
print ("</body>")
print ("</html>")



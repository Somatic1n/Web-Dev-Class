#! C:\Python313\python.exe

import os
import urllib.parse
import mysql.connector # must install mysql-connector-python then mysql-connector
from mysql.connector import errorcode
from  DBConnection import HOST, USER, PASSWORD, DATABASE, AUTHPLUGIN

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

#**********Execute the SQL Statement**********

mycursor.execute("SELECT * FROM user")
myresult = mycursor.fetchall()

#**********Output HTML**********

print ("Content-type:text/html\r\n\r\n")
print ("<!DOCTYPE html>")
print ("<html>")
print ("<head>")
print ("<title>Python Crud Read</title>")
print ("</head>")
print ("<body>")

for x in myresult:
  print(x)
  print("<br>")
mydb.close()

print ("<br><br><a href='index.html'>Crud Home</a>")  
print ("</body>")
print ("</html>")
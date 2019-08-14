#!/usr/bin/python


import sqlite3,os,re,sys,optparse


print("""
++++++++++++++++++++++++++++++++++
SVN Database History Reader
Author: Alaa Abdulridha
Contact: https://alaa.blog
+++++++++++++++++++++++++++++++++++
""")
database = input("Enter db patch and name ex. c:\wc.db:")
Logname = input("Enter The output file name ex. output.txt:")

conn = sqlite3.connect(database)
cursor = conn.cursor()
cursor.execute("select local_relpath,kind, changed_author, checksum from NODES")
with open (Logname, "w", newline='') as f:
    for row in cursor:
        print(row[0],row[1],row[2],row[3], file=f)
        print(row)
rows = cursor.fetchall()






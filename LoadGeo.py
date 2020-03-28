import urllib.request, urllib.parse, urllib.error
import json
import sqlite3
import ssl

datahandle=sqlite3.connect('Rawdata.sqlite')
cur=datahandle.cursor()

#URl elements being figured out
serviceurl="https://maps.googleapis.com/maps/api/geocode/json?"
api_key='AIzaSyDVoOJTUOsz3pDCzCKMFdrY5qSnCC-xzSU'

#Creates a table in our database and remove existing table
cur.execute('DROP TABLE IF EXISTS Locations')

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


filehandle=open("where.data")
for line in filehandle:
    text=line.strip()
    values=dict()
    values["address"]=text
    values['key']=api_key
    finalurl=serviceurl+urllib.parse.urlencode(values)

    urlhandle=urllib.request.urlopen(finalurl,context=ctx)
    data=urlhandle.read().decode()
    print("FOR address:",text,"the json we got was as follows:\n",data)
    print("\n\n\n\n")

    cur.execute('INSERT OR IGNORE INTO Locations(address, geodata) VALUES(?,?)',(memoryview(text.encode()),memoryview(data.encode())))
    datahandle.commit()

print("All entries are now successfully stored in the database, run a cleanup code to make sense out of it")

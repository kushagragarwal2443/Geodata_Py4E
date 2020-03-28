import json
import sqlite3
import codecs

filehandle=codecs.open("where.js","w","utf-8")
filehandle.write("myData = [\n")
flag=0

datahandle=sqlite3.connect('Rawdata.sqlite')
cur=datahandle.cursor()
cur.execute('SELECT * FROM Locations')

for row in cur:

    if(flag==1):
        filehandle.write(",\n")
    flag=1

    text=row[1].decode()
    strtext=str(text)
    js=json.loads(strtext)

    lat=js['results'][0]['geometry']['location']['lat']
    lon=js['results'][0]['geometry']['location']['lng']
    addfinal=js['results'][0]['formatted_address']
    addfinal=addfinal.replace("'", "")
    print(addfinal,lat,lon)

    towrite="["+str(lat)+","+str(lon)+", '"+addfinal+"']"
    filehandle.write(towrite)

filehandle.write("\n];\n")
datahandle.close()
filehandle.close()

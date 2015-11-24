#!/usr/bin/python3
#A script to create html report page of out MongoDB query results
#Usage: ./html_page.py [json] > out.html

import json
import operator
import sys
import re

if(len(sys.argv)<2):
    sys.exit("Usage: ./html_page.py [json] > out.html")

jfile=open(sys.argv[1], "r")
temp_file=open("temp.html", "r")

line = jfile.readline()
jlist=json.loads(line)
sorted_x=sorted(jlist.items(), key=operator.itemgetter(1), reverse=True)
jfile.close()

color_list=["#2484c1","#0c6197","#4daa4b","#90c469","#daca61","#e4a14b","#e98125","#cb2121","#830909","#923e99"]

read_sum=0
for spec in sorted_x:
    read_sum+=spec[1]

for line in temp_file.readlines():
    line=line.rstrip()
    if( re.search("Sample 181V3A", line) ):
        sample_name = sys.argv[1].split(".")[0]
        print("\t\t\t\"text\": \"Fungal MongoDB Query Hits -- Sample "+sample_name+"\",")
    elif( re.search("</tr>", line) ):
        print(line)
        for spec in sorted_x[0:20]:
            print("<tr>")
            print("\t<td>"+spec[0]+"</td>")
            print("\t<td>"+str(spec[1])+"</td>")
            print("\t<td>"+str(spec[1]/read_sum*1000000)+"</td>")
            print("</tr>")
    elif( re.search("content\": \[", line)):
        print(line)
        i=0
        for spec in sorted_x[1:11]:
            print("\t\t\t{")
            print("\t\t\t\t\"label\": \""+spec[0]+"\",")
            print("\t\t\t\t\"value\": "+str(spec[1])+",")
            print("\t\t\t\t\"color\": \""+color_list[i]+"\"")
            print("\t\t\t},")
            i+=1
    else:
        print(line)       

temp_file.close()

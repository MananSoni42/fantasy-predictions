import csv
import json
import time
import re
import requests
from pprint import pprint
from bs4 import BeautifulSoup

stadium_ids={
    0:"arunjaitleystats",
    1:"MAChidambaram",
    2:"narendrimodi",
    3:"wankhede",
    4:"mchinnaswamy",
    5:"edengardensstats",
}

id2tag = {
    0: { 'std-id': 0, 'table-start': 1, '2021': True },
    1: { 'std-id': 3, 'table-start': 1, '2021': True },
    2: { 'std-id': 4, 'table-start': 1, '2021': True },
    3: { 'std-id': 5, 'table-start': 1, '2021': True },
    4: { 'std-id': 2, 'table-start': 0, '2021': False },
    5: { 'std-id': 1, 'table-start': 0, '2021': False },
}

def stadium_records(stadium_url):
    r = requests.get(stadium_url)
    soup = BeautifulSoup(r.content, 'lxml')
    stadium_record = []
    tag = soup.find_all('h2')

    for stid in stadium_ids:
        row = []
        row.append(tag[ id2tag[stid]['std-id'] ].text)
        text1 = soup.find('figure',id=stadium_ids[stid])
        for i in range(id2tag[stid]['table-start'], id2tag[stid]['table-start']+8):
            #print(stid,i)
            try:
                row.append(text1.table.tbody('tr')[i]('td')[1].text)
                if id2tag[stid]['2021']:
                    row.append(text1.table.tbody('tr')[i]('td')[2].text)
                else:
                    row.append('-')
            except:
                print(text1.table.tbody.prettify())
        #row = [row[0], *row[1], *row[2]]
        stadium_record.append(row)
    return stadium_record

url='https://t20-head-to-head.com/statistics-by-ipl-venue/'

stadium_headers = [ 'Stadium name' ]
template_header = ['Average first innings score', 'Average first innings winning score', '% Teams winning batting first', '% Teams winning chasing', 'balls per 4 scored', 'balls per 6 scored ', 'Average powerplay score', 'Average death overs (last 5) score']
for header in template_header:
    for i in range(2):
        stadium_headers.append('All time ' + header if i%2==0 else '2021 ' + header)

with open('stadium_record.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(stadium_headers)
        writer.writerows(stadium_records(url))

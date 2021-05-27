import csv
import json
import time
import re
import requests
from pprint import pprint
from bs4 import BeautifulSoup
clean = lambda x: x.lower().replace(' ','').replace('\n','')
def sr_100(sr_url):
    r = requests.get(sr_url)
    soup = BeautifulSoup(r.content, 'lxml')
    sr={
        'stats':[],
    }
    player_name=[]
    for tag in soup.findAll('div', attrs={'class': 'top-players__player-name'}):
        if(tag.find('a', attrs={'class': 'top-players__player-link'})):
            new_tag = tag.find('a', attrs={'class': 'top-players__player-link'})
            player_name.append(clean(new_tag.text))
        else:
            player_name.append(clean(tag.text))
    for table in soup('table'):
        row=1
        k=-1
        for row in table('tr'):
            i=0
            curr_row = []
            for col in row('td'):
                if(i!=1):
                    curr_row.append(clean(col.text))
                if(i==1):
                    curr_row.append(curr_row.append(player_name[k]))
                    print(k)
                i=i+1
            sr['stats'].append(curr_row) 
            k=k+1
    return sr
header_player_sr_100=['sr.no','player','matches','innings','not-outs','Runs scored','Highest Score','Average','BF','Strike-rate','100s','50s','4s','6s']
sr_records_100=[]

url_sr="https://www.iplt20.com/stats/all-time/best-batting-strike-rate"
sr=sr_100(url_sr)
for record in sr['stats']:
    sr_records_100.append(record)
   
with open('top_100_strike_rate.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header_player_sr_100)
        writer.writerows(sr_records_100)

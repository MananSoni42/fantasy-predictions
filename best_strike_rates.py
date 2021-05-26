import csv
import json
import time
import re
import requests
from pprint import pprint
from bs4 import BeautifulSoup

def strike_rate(sr_url):
    r = requests.get(sr_url)
    soup = BeautifulSoup(r.content, 'lxml')
    sr={
        'stats':[],
    }
    j=0
    k=0
    for table in soup('table'):
        j=j+1
        print(1)
        if table.get('class',[]) and 'engineTable' in table['class']:
            for row in table.tbody('tr'):
                if(k%2==0):
                    curr_row = []
                    for col in row('td'):
                        curr_row.append(col.text)
                    sr['stats'].append(curr_row)
                k=k+1
        if(j==1):
            break
        
    return sr
header_player_sr=['player','span','matches','innings','not-outs','Runs scored','Highest Score','Average','BF','Strike-rate','100s','50s','0s','4s','6s']
sr_records=[]

url_sr="https://stats.espncricinfo.com/ci/engine/records/batting/highest_career_strike_rate.html?id=117;type=trophy"
records_backup=strike_rate(url_sr)
for record in records_backup['stats']:
    sr_records.append([*record])
   
with open('best_strike_rate_player.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header_player_sr)
        writer.writerows(sr_records)

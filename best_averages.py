import csv
import json
import time
import re
import requests
from pprint import pprint
from bs4 import BeautifulSoup

def averages(avg_url):
    r = requests.get(avg_url)
    soup = BeautifulSoup(r.content, 'lxml')
    avg={
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
                    avg['stats'].append(curr_row)
                k=k+1
        if(j==1):
            break
        
    return avg
header_player_ave=['player','span','matches','innings','not-outs','Runs scored','Highest Score','Average','BF','Strike-rate','100s','50s','0s','4s','6s']
avg_records=[]

url_ave="https://stats.espncricinfo.com/ci/engine/records/batting/highest_career_batting_average.html?id=117;type=trophy"
records_backup=averages(url_ave)
for record in records_backup['stats']:
    avg_records.append([*record])
   
with open('avg_player.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header_player_ave)
        writer.writerows(avg_records)

import csv
import json
import time
import re
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from Player_form import *

def overall_record_backup(overall_url_backup):
    r = requests.get(overall_url_backup)
    soup = BeautifulSoup(r.content, 'lxml')
    overall_record_backup={
        'player_name':'',
        'stats':[],
    }
    overall_record_backup['player_name']=soup.find('div', {"class":'player-card'}).h2.text
    j=0
    for table in soup('table'):
        j=j+1
        if table.get('class',[]) and 'standings-widget-table' in table['class']:
            title = soup.find('h5', class_='border-bottom-gray-300').get_text()
            print(title)
            if(title=='Batting & Fielding'):
                for row in table.tbody('tr'):
                    curr_row = []
                    for col in row('td'):
                        curr_row.append(col.text)
                    overall_record_backup['stats'].append(curr_row)
            else:
                print("Bowling hehe")
        if(j==1):
            break
        
    return overall_record_backup
header_player_record_backup=['player-name','format','matches','innings','not-outs','Runs scored','Highest Score','Average','BF','Strike-rate','100s','50s','4s','6s','Catches','Stumpings']
bat_records_backup=[]
i=0
for i in range(193):
    url_backup = players_url[i]
    records_backup=overall_record_backup(url_backup)
    for record in records_backup['stats']:
        bat_records_backup.append([records_backup['player_name'],*record])
   
with open('player_batting_record_backup.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header_player_record_backup)
        writer.writerows(bat_records_backup)

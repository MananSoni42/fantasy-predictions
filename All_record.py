import csv
import json
import time
import re
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from Player_form import *

def overall_record(overall_url):
    r = requests.get(overall_url)
    soup = BeautifulSoup(r.content, 'lxml')
    overall_record={
        'player_name':[],
        'runs':[],
        'average':[],
        'strike-rate':[],
    }
    overall_record['player_name'].append(soup.find('div', {"class":'player-card'}).h2.text)
    for table in soup('table'):
        if table.get('class',[]) and 'standings-widget-table' in table['class']:
            overall_record['runs'].append(table.tbody('tr')[2]('td')[4].text)
            overall_record['average'].append(table.tbody('tr')[2]('td')[6].text)
            overall_record['strike-rate'].append(table.tbody('tr')[2]('td')[8].text)
    overall_record['runs']=overall_record['runs'][0]
    overall_record['average']=overall_record['average'][0]
    overall_record['strike-rate']=overall_record['strike-rate'][0]        
    return overall_record
header_player_record=['player-name','runs-scored','average','strike-rate']
bat_records=[]
i=0
for i in range(96):
    url = players_url[i]
    records=overall_record(url)
    bat_records.append([records['player_name'],records['runs'],records['average'],records['strike-rate']])
with open('player_batting_record.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header_player_record)
        writer.writerows(bat_records)

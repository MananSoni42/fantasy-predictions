import csv
import json
import time
import re
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from Player_form import *
from time import sleep
from utils import clean

def get_role_str(divs):
    for div in divs:
        if clean(div.p.text) == 'playing-role':
            return get_role(div.h5.text)
    raise Exception('No playing role found')

def get_role(role):
    role = clean(role).split('-')
    wk = 'wicketkeeper' in role
    if 'allrounder' in role:
        return 'all', wk
    elif 'batter' in role or 'batsman' in role or 'wicketkeeper' in role:
        return 'bat', wk
    elif 'bowler' in role or 'arm' in role or 'legbreak' in role or 'break' in role or 'spin' in role:
        return 'bowl', wk
    else:
        raise Exception(f'No: `{role}`')

def overall_record_backup(overall_url_backup):
    r = requests.get(overall_url_backup)
    soup = BeautifulSoup(r.content, 'lxml')
    overall_record_backup={
        'player_name': '',
        'role': '',
        'wk': False,
        'stats-bat': {},
        'stats-bowl': {},
    }

    bat_row = {
        'test': ['-']*14,
        't20i': ['-']*14,
        'odi': ['-']*14,
        'fc': ['-']*14,
        'list a': ['-']*14,
        't20': ['-']*14,
    }
    bowl_row = {
        'test': ['-']*13,
        't20i': ['-']*13,
        'odi': ['-']*13,
        'fc': ['-']*13,
        'list a': ['-']*13,
        't20': ['-']*13,
    }

    for table in soup('table'):
        if table.get('class',[]) and 'standings-widget-table' in table['class']:
            title = table.parent.parent.find('h5', class_='border-bottom-gray-300').get_text()
            title = clean(title)
            #print(f'`{title}`')
            if title == 'batting-&-fielding':
                for row in table.tbody('tr'):
                    btrow = []
                    for col in row('td'):
                        btrow.append(col.text)
                    bat_row[clean(btrow[0])] = btrow[1:]
            elif title == 'bowling':
                for row in table.tbody('tr'):
                    bwrow = []
                    for col in row('td'):
                        bwrow.append(col.text)
                    bowl_row[clean(bwrow[0])] = bwrow[1:]
            else:
                raise Exception('No')

    overall_record_backup['player_name']=soup.find('div', {"class":'player-card'}).h2.text
    role, wk = get_role_str(soup.find('div', {"class":'player_overview-grid'})('div'))
    overall_record_backup['role'] = role
    overall_record_backup['wk'] = wk
    overall_record_backup['stats-bat'] = bat_row
    overall_record_backup['stats-bowl'] = bowl_row
    return overall_record_backup

header_player_record_backup=['player-name', 'WK', 'role', 'format'] +\
    ['matches','innings','not-outs','Runs scored','Highest Score','Average','BF','Strike-rate','100s','50s','4s','6s','Catches','Stumpings'] +\
    ['Mat', 'Inns', 'Balls', 'Runs', 'Wkts', 'BBI', 'BBM', 'Ave', 'Econ', 'SR', '4w', '5w', '10w']

bat_records_backup=[]

for i,url_backup in players_url.items():
    records_backup=overall_record_backup(url_backup)
    name = clean(records_backup['player_name'])
    sleep(0.5)
    print(i,name, records_backup['role'], 'wk' if records_backup['wk'] else '')
    for key in records_backup['stats-bat'].keys():
        row = [key] + records_backup['stats-bat'][key] + records_backup['stats-bowl'][key]
        bat_records_backup.append([records_backup['player_name'],
                                   int(records_backup['wk']),
                                   records_backup['role'],
                                   *row])

with open('player_batting_record_backup.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header_player_record_backup)
        writer.writerows(bat_records_backup)

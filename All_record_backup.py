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
        'player_name':[],
        'stats':[],
    }
    overall_record_backup['player_name'].append(soup.find('div', {"class":'player-card'}).h2.text)
    for table in soup('table'):
        if table.get('class',[]) and 'standings-widget-table' in table['class']:
            for row in table.tbody('tr'):
                curr_row = []
                for col in row('td'):
                    curr_row.append(col.text)
                overall_record_backup['stats'].append(curr_row)
        
    return overall_record_backup
header_player_record_backup=['player-name','format','matches','innings','not-outs','Runs scored','Highest Score','Average','BF','Strike-rate','100s','50s','4s','6s','Catches','Stumpings']
bat_records_backup=[]
data = []*5
i=0
for i in range(194):
    url_backup = players_url[i]
    records_backup=overall_record_backup(url_backup)
    bat_records_backup.append([records_backup['player_name'],records_backup['stats']])
   # print(records_backup)
    #for j in range(3):
   # curr_row = [0]*16
   # curr_row[0]=records_backup['player_name'] 
   # curr_row[1]=records_backup['stats'][i][0]
   # curr_row[2]=records_backup['stats'][i][1]
   # curr_row[3]=records_backup['stats'][i][2]
   # curr_row[4]=records_backup['stats'][i][3]
   # curr_row[5]=records_backup['stats'][i][4]
   # curr_row[6]=records_backup['stats'][i][5]
   # curr_row[7]=records_backup['stats'][i][6]
   # curr_row[8]=records_backup['stats'][i][7]
   # curr_row[9]=records_backup['stats'][i][8]
   # curr_row[10]=records_backup['stats'][i][9]
   # curr_row[11]=records_backup['stats'][i][10]
   # curr_row[12]=records_backup['stats'][i][11]
   # curr_row[13]=records_backup['stats'][i][12]
   # curr_row[14]=records_backup['stats'][i][13]
   # curr_row[15]=records_backup['stats'][i][14]
    #data.extend(curr_row)
#bat_records_backup.append(data)

with open('player_batting_record_backup.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header_player_record_backup)
        writer.writerows(bat_records_backup)

import csv
import json
import time
import re
import requests
from pprint import pprint
from bs4 import BeautifulSoup

def powerplay_records(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    powerplay_record={
        'Statistic_name':[],
        'Team':[],
        'avg_pp_scr':[],
        'avg_pp_wickt_lst':[],
    }
    current_header=[]
    tag = soup.find_all('h5')
    current_header.append(tag[0].text)
    print(current_header) 
    #stadium_record['stadium_name'].append(current_header)
    #for stid in stadium_ids:
        #text1 = soup.find('figure',id=stadium_ids[stid])
        #for i in range(1,9):
            #stadium_record['Bat_Statistic'].append(text1.table.tbody('tr')[i]('td')[0].text)
            #stadium_record['Bat_All-time'].append(text1.table.tbody('tr')[i]('td')[1].text)
            #stadium_record['Bat_2021'].append(text1.table.tbody('tr')[i]('td')[2].text)
    #for table in soup('table'):
        #if table.get('class',[]):
     #   print('hi')
     #   stadium_record['Bat_Statistic'].append(table.tbody('tr')[0]('td')[0].text)
     #   stadium_record['Bat_All-time'].append(table.tbody('tr')[0]('td')[1].text)
     #   stadium_record['Bat_2021'].append(table.tbody('tr')[0]('td')[2].text)
    return powerplay_record
#data=[]   
url='https://t20-head-to-head.com/powerplay-stats-ipl-2021/s'
powerplay_record_store=powerplay_records(url)
#stadium_headers=['stadium_name','batting_statistic','batting_all_time','Batting_2021']
#data.append([stadium_record_store['stadium_name'],stadium_record_store['Bat_Statistic'],stadium_record_store['Bat_All-time'],stadium_record_store['Bat_2021']])


#with open('stadium_record.csv', 'w') as f:
        #writer = csv.writer(f)
        #writer.writerow(stadium_headers)
        #writer.writerows(data)

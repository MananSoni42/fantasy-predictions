import csv
import json
import time
import re
import requests
from pprint import pprint
from bs4 import BeautifulSoup
clean = lambda x: x.lower().replace(' ','').replace('\n','')
def averages_100(avg_url):
    r = requests.get(avg_url)
    soup = BeautifulSoup(r.content, 'lxml')
    avg={
        'stats':[],
    }
    #for j in range(100):
    player_name=[]
    for tag in soup.findAll('div', attrs={'class': 'top-players__player-name'}):
        if(tag.find('a', attrs={'class': 'top-players__player-link'})):
            new_tag = tag.find('a', attrs={'class': 'top-players__player-link'})
            player_name.append(clean(new_tag.text))
        else:
            player_name.append(clean(tag.text))
    #print(player_name)
    for table in soup('table'):
        #if table.get('class',[]) and 'table--scroll-on-tablet top players' in table['class']:
        #print(table('tr'))
        row=1
        #p_name = soup.find('div', {"class":'top-players__player-name'}).text
        #print(clean(p_name))
        k=-1
        for row in table('tr'):
            #print(row)
            i=0
            curr_row = []
            for col in row('td'):
                if(i!=1):
                    curr_row.append(clean(col.text))
                if(i==1):
                    #p_name = soup.find('div', {"class":'top-players__player-name'}).text
                    #print(clean(p_name))
                    curr_row.append(player_name[k])
                    print(k)
                i=i+1
            avg['stats'].append(curr_row)
            k=k+1
    return avg
header_player_ave_100=['sr.no','player','matches','innings','not-outs','Runs scored','Highest Score','Average','BF','Strike-rate','100s','50s','4s','6s']
avg_records_100=[]

url_ave="https://www.iplt20.com/stats/all-time/best-batting-average"
records_backup_ave=averages_100(url_ave)
for record in records_backup_ave['stats']:
    avg_records_100.append(record)
   
with open('avg_player_100.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header_player_ave_100)
        writer.writerows(avg_records_100)

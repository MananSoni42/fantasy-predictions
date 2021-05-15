import csv
import json
import time
import re
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from utils import *

get_num = lambda x: int(''.join(c for c in x if c.isdigit()))
player_id = {
    'next-id': 1,
}

season_url = {
    2021: 'https://www.espncricinfo.com/series/ipl-2021-1249214/match-results',
    2020: 'https://www.espncricinfo.com/series/ipl-2020-21-1210595/match-results',
    2019: 'https://www.espncricinfo.com/series/ipl-2019-1165643/match-results',
    2018: 'https://www.espncricinfo.com/series/ipl-2018-1131611/match-results',
    2017: 'https://www.espncricinfo.com/series/ipl-2017-1078425/match-results',
}

def get_all_match_urls(season):
    url = season[url]
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    matches = []
    ipl_matches = soup.find('div', {"class": lambda x: x and 'series-results-page-wrapper' in x.split()})
    for div in ipl_matches.find_all('a', {"class": lambda x: x and 'match-info-link-FIXTURES' in x.split()}):
        status = div.find('div', {"class": lambda x: x and 'status' in x.split()}).text
        link = div['href']
        num = div.find('div', {"class": lambda x: x and 'description' in x.split()}).text.split()[0]
        matches.append({
            'status': status,
            'season': season,
            'number': get_num(num),
            'url': url,
        })
    return matches

def get_espn_scorecard(match_url, save=False):

    r = requests.get(match_url)
    soup = BeautifulSoup(r.content, 'lxml')

    scorecard = {
        'batsman': [],
        'batsman_header': [],
        'bowler': [],
        'bowler_header': [],
        'toss': '',
        'stadium': '',
    }

    for table in soup('table'):
        if table.get('class',[]) and 'match-details-table' in table['class']:
            scorecard['toss'] = table.tbody('tr')[1]('td')[1].text
            scorecard['stadium'] = table.tbody.tr.td.text
        elif table.get('class',[]) and ('batsman' in table['class'] or 'bowler' in table['class']):
            if not scorecard['batsman_header'] and 'batsman' in table['class']:
                scorecard['batsman_header'] = [h.text for h in table.thead.tr('th')]
            if not scorecard['bowler_header'] and 'bowler' in table['class']:
                scorecard['bowler_header'] = [h.text for h in table.thead.tr('th')]

            for row in table.tbody('tr'):
                curr_row = []
                for col in row('td'):
                    curr_row.append(col.text)
                if 'batsman' in table['class']:
                    scorecard['batsman'].append(curr_row)
                else:
                    scorecard['bowler'].append(curr_row)

    return scorecard

def process_players(match, scorecard):
    players = set()
    for batsman in scorecard['batsman']:
        name = clean(batsman[0])
        if name and name != 'extras':
            players.add(name)
            out,_,wicket_players = get_wicket_info(batsman[1])
            for player in wicket_players:
                players.add(player)
    for bowler in scorecard['bowler']:
        players.add(clean(bowler[0]))

    data_row = [0]*22
    data = []
    for player in player:
        if player in player_id:
            id = player_id[player]
        else:
            id = player_id['next-id']
            player_id[id] = player
        curr_row = data_row.copy()
        curr_row[0] = id
        curr_row[1] = match['season']
        curr_row[2] = match['number']


def ipl_season_csv():
    header = ['player-id', 'season', 'match'] + \
             ['batting-runs', 'balls', 'out', '4s', '6s', 'sr'] + \
             ['overs', 'maiden', 'bowling-runs', 'wicket-bowled', 'wicket-catch', 'wicket-lbw', 'econ', '0s', '4s', '6s'] + \
             ['catches', 'run-out', 'stumping']

    data = []
    header_meta = ['season', 'match', 'status', 'toss-team', 'toss-decision', 'venue']
    metadata = []

    for season in season_url:
        print(f'Season - {season}')
        matches = get_all_match_urls(season)
        for match in matches:
            time.sleep(0.2)
            print(f'\t Match - {match["number"]}')
            scorecard = get_espn_scorecard(match['url'])
            metadata.append(match['season'], match['number'], match['status'], *get_toss_info(scorecard['toss']))

#pprint(get_all_match_urls())
scorecard = get_espn_scorecard('https://www.espncricinfo.com/series/ipl-2021-1249214/mumbai-indians-vs-royal-challengers-bangalore-1st-match-1254058/full-scorecard')
print(scorecard['batsman_header'])
print(scorecard['bowler_header'])
print(scorecard['batsman'][0])
pprint(process_scorecard(scorecard))

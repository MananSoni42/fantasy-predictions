import csv
import json
import time
import re
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from utils import *

def get_all_match_urls(season):
    '''
    Get match URLS and basic details from a list of links for each season.
    This list is defined in `utils.py`
    '''

    url = season_url[season]
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    matches = []
    ipl_matches = soup.find('div', {"class": lambda x: x and 'series-results-page-wrapper' in x.split()})
    for div in ipl_matches.find_all('a', {"class": lambda x: x and 'match-info-link-FIXTURES' in x.split()}):
        try:
            status = div.find('div', {"class": lambda x: x and 'status' in x.split()}).text
            link = div['href']
            num = div.find('div', {"class": lambda x: x and 'description' in x.split()}).text.split()[0]
            matches.append({
                'status': status,
                'season': season,
                'number': get_num(num),
                'url': 'https://www.espncricinfo.com' + link,
            })
        except:
            print('Error in getting a match')
    return matches

def get_espn_scorecard(match_url):
    '''
    Creates a basic scorecard (dictionary) from a URL for the match (from ESPN cricinfo)
    '''
    r = requests.get(match_url)
    soup = BeautifulSoup(r.content, 'lxml')

    squad = {
        0: {
            'wk': '',
            'players': set(),
        },
        1: {
            'wk': '',
            'players': set(),
        },
    }
    innings = 0

    scorecard = {
        'batsman': [],
        'bowler': [],
        'toss': '',
        'stadium': '',
    }

    for table in soup('table'):
        if table.get('class',[]) and 'match-details-table' in table['class']:
            scorecard['toss'] = table.tbody('tr')[1]('td')[1].text
            scorecard['stadium'] = table.tbody.tr.td.text
        elif table.get('class',[]) and ('batsman' in table['class'] or 'bowler' in table['class']):
            for row in table.tbody('tr'):
                player = clean_not_wk(row.td.text)
                if player and player!='extras' and 'batsman' in table['class']:
                    if '†' in player:
                        squad[innings//2]['wk'] = clean(player)
                    squad[innings//2]['players'].add(clean(player))
                curr_row = []
                for col in row('td'):
                    curr_row.append(col.text)
                if 'batsman' in table['class']:
                    scorecard['batsman'].append(curr_row)
                else:
                    scorecard['bowler'].append(curr_row)

            try:
                for pl in table.tfoot('tr')[1]('a'):
                    player = clean_not_wk(pl.text)
                    if player and player!='extras':
                        if '†' in player:
                            squad[innings//2]['wk'] = clean(player)
                        squad[innings//2]['players'].add(clean(player))
            except:
                pass
            innings += 1

    return scorecard, squad

def process_players(match, scorecard):
    '''
    Convert a given scorecard into data format that is compatible with the CSV
    Each player has a unique player id (stored in data-players.json)
    Returns a 2-d array
    '''
    global player_id
    players = set()
    for batsman in scorecard['batsman'] + scorecard['bowler']:
        name = clean(batsman[0])
        if name and name != 'extras':
            players.add(name)

    for batsman in scorecard['batsman']:
        name = clean(batsman[0])
        if name and name != 'extras':
            out,_,wicket_players = get_wicket_info(batsman[1])
            for player in wicket_players:
                found, close_player = find_closest(player, players)
                if found:
                    players.add(close_player)
                elif clean(player) in alt_players:
                    players.add(alt_players[clean(player)])
                else:
                    print(f'player name error: {player} did not match \nclosest: {close_player}')

    data_row = [0]*20
    data = dict()
    for player in players:
        if player in player_id:
            id = player_id[player]
        else:
            id = player_id['next-id']
            player_id['next-id'] += 1
            player_id[player] = id
        curr_row = data_row.copy()
        curr_row[0] = id
        curr_row[1] = match['season']
        curr_row[2] = match['number']
        data[id] = curr_row

    for batsman in scorecard['batsman']:
        name = clean(batsman[0])
        if name and name != 'extras':
            id = player_id[name]
            out, type, wicket_players = get_wicket_info(batsman[1])
            data[id][3] = int(batsman[2])
            data[id][4] = int(batsman[3])
            data[id][5] = int(out)
            data[id][6] = int(batsman[5])
            data[id][7] = int(batsman[6])
            data[id][8] = float(batsman[7])
            for player in wicket_players:
                found, close_player = find_closest(player, players)
                if found:
                    id = player_id[close_player]
                    if type == 'catch':
                        data[id][17] += 1
                    elif type == 'run-out':
                        data[id][18] += 1
                elif clean(player) in alt_players:
                    id = player_id[alt_players[clean(player)]]
                else:
                    print(f'player name error: {player} did not match \nclosest: {close_player}')

    for bowler in scorecard['bowler']:
        name = clean(bowler[0])
        if name:
            id = player_id[name]
            data[id][9] = float(bowler[1])
            data[id][10] = int(bowler[2])
            data[id][11] = int(bowler[3])
            data[id][12] = int(bowler[4])
            data[id][13] = float(bowler[5])
            data[id][14] = int(bowler[6])
            data[id][15] = int(bowler[7])
            data[id][16] = int(bowler[8])
    return list(data.values())

def ipl_season_csv():
    '''
    Combine everything to create csv files from a list of season URLS
    '''

    header = ['player-id', 'season', 'match'] + \
             ['batting-runs', 'balls', 'out', '4s', '6s', 'sr'] + \
             ['overs', 'maiden', 'bowling-runs', 'wickets', 'econ', '0s', '4s', '6s'] + \
             ['catches', 'run-out', 'stumping']

    data = []
    header_meta = ['season', 'match', 'status', 'toss-team', 'toss-decision', 'venue']
    metadata = []

    for season in season_url:
        print(f'Season - {season}')
        matches = get_all_match_urls(season)
        for match in matches:
            time.sleep(0.2)
            try:
                scorecard = get_espn_scorecard(match['url'])
                metadata.append([match['season'], match['number'], match['status'], *get_toss_info(scorecard['toss']), scorecard['stadium']])
                data.extend(process_players(match,scorecard))
                print(f'\t Match - {match["number"]} success')
            except:
                print(f'\t Match - {match["number"]} fail')

    with open('data-match.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    with open('data-meta.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header_meta)
        writer.writerows(metadata)

    with open('data-players.json', 'w') as f:
        json.dump(player_id, f, indent=4)

matches = get_all_match_urls(2021)
match = matches[-1]
scorecard,squad = get_espn_scorecard(match['url'])
pprint(squad)
#print(match)
#print(scorecard)
#pprint(process_players(match,scorecard))
#ipl_season_csv()

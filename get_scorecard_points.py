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
            num = div.find('div', {"class": lambda x: x and 'description' in x.split()}).text.lower().split()
            try:
                num = get_num(num[0]) # regular IPL match
            except:
                if 'final' in num:
                    num = 60
                elif 'eliminator' in num:
                    num = 58
                elif 'qualifier' in num:
                    if num[1] == '1':
                        num = 57
                    else:
                        num = 59
                else:
                    print(f'Could not understand match number: `{" ".join(num)}`')


            matches.append({
                'status': status,
                'season': season,
                'number': num,
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
        'batsman': {
            0: [],
            1: [],
        },
        'bowler': {
            0: [],
            1: [],
        },
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
                    scorecard['batsman'][innings//2].append(curr_row)
                else:
                    scorecard['bowler'][innings//2].append(curr_row)

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

def try_catch(func, val):
    try:
        return func(val)
    except:
        return 0

def process_players(match, scorecard, squad):
    '''
    Convert a given scorecard into data format that is compatible with the CSV
    Each player has a unique player id (stored in data-players.json)
    Returns a 2-d array
    '''
    data_row = [0]*20
    data = dict()

    for innings in [0,1]:
        for player in squad[innings]['players']:
            data[player] = data_row.copy()
            data[player][0] = player

    for innings in [0,1]:
        for batsman in scorecard['batsman'][innings]:
            name = clean(batsman[0])
            if name and name != 'extras':
                id = name
                out, type, wicket_players = get_wicket_info(batsman[1])
                data[id][0] = name
                data[id][1] = match['season']
                data[id][2] = match['number']
                data[id][3] = try_catch(int, batsman[2])
                data[id][4] = try_catch(int, batsman[3])
                data[id][5] = try_catch(int, out)
                data[id][6] = try_catch(int, batsman[5])
                data[id][7] = try_catch(int, batsman[6])
                data[id][8] = try_catch(float, batsman[7])
                for player in wicket_players:
                    found, close_player = find_closest_with_inn(player, innings, squad)
                    if found:
                        id = close_player
                        if type == 'catch':
                            data[id][17] += 1
                        elif type == 'run-out':
                            if name == squad[innings]['wk']:
                                data[id][19] += 1
                            else:
                                data[id][18] += 1
                    elif clean(player) in alt_players:
                        id = clean(alt_players[clean(player)])
                        if type == 'catch':
                            data[id][17] += 1
                        elif type == 'run-out':
                            if name == squad[innings]['wk']:
                                data[id][19] += 1
                            else:
                                data[id][18] += 1
                    else:
                        print(f'player name error: {player} did not match \nclosest: {close_player}')

        for bowler in scorecard['bowler'][innings]:
            name = clean(bowler[0])
            if name:
                id = name
                data[id][9] = try_catch(float, bowler[1])
                data[id][10] = try_catch(int, bowler[2])
                data[id][11] = try_catch(int, bowler[3])
                data[id][12] = try_catch(int, bowler[4])
                data[id][13] = try_catch(float, bowler[5])
                data[id][14] = try_catch(int, bowler[6])
                data[id][15] = try_catch(int, bowler[7])
                data[id][16] = try_catch(int, bowler[8])

    return list(data.values())

def ipl_season_csv():
    '''
    Combine everything to create csv files from a list of season URLS
    '''

    header = ['player-name', 'season', 'match'] + \
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
            if 'postponed' in match['status'].lower():
                print(f'\t Match - {match["number"]} postponed')
                continue
            elif 'abandoned' in match['status'].lower():
                print(f'\t Match - {match["number"]} abandoned')
                continue
            time.sleep(0.2)
            scorecard, squad = get_espn_scorecard(match['url'])
            metadata.append([match['season'], match['number'], match['status'], *get_toss_info(scorecard['toss']), scorecard['stadium']])
            data.extend(process_players(match, scorecard, squad))
            print(f'\t Match - {match["number"]} done')

    with open('data-match.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    with open('data-meta.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header_meta)
        writer.writerows(metadata)

'''
matches = get_all_match_urls(2017)
match = matches[-29]
scorecard,squad = get_espn_scorecard(match['url'])
pprint(process_players(match,scorecard,squad))
'''

ipl_season_csv()

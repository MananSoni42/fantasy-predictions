import csv
import requests
from pprint import pprint
from bs4 import BeautifulSoup

def get_all_match_urls():
    url = 'https://www.espncricinfo.com/series/ipl-2021-1249214/match-results'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    matches = []
    ipl_matches = soup.find('div', {"class": lambda x: x and 'series-results-page-wrapper' in x.split()})
    for div in ipl_matches.find_all('a', {"class": lambda x: x and 'match-info-link-FIXTURES' in x.split()}):
        status = div.find('div', {"class": lambda x: x and 'status' in x.split()}).text
        link = div['href']
        matches.append({
            'status': status,
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


pprint(get_all_match_urls())
#scorecard = get_espn_scorecard('https://www.espncricinfo.com/series/ipl-2021-1249214/mumbai-indians-vs-royal-challengers-bangalore-1st-match-1254058/full-scorecard')
#pprint(scorecard)

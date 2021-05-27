import re
import json
from difflib import SequenceMatcher

''' cleans a string (removes whitespace, extra characters, etc '''
clean = lambda s: s.lower().replace('(c)','').replace('†','').replace(u'\xa0', u' ').rstrip().lstrip().replace(' ','-').rstrip('-')
clean_not_wk = lambda s: s.lower().replace('(c)','').replace(u'\xa0', u' ').rstrip().rstrip(',').lstrip().replace(' ','-')

''' Convert string of toss into which team won it and decided to bat/bowl '''
get_toss_info = lambda toss: (clean(toss.split(',')[0]), 'bat' if 'bat' in toss.split() else 'bowl')

def get_wicket_info(wicket_str):
    '''
    Take string describing the wicket (like `b Chahar` or `run out (kohli/bumrah)`) and
    convert into meaningful information.
    Returns
        - whether it was out or not out
        - type of wicket: run-out / catch / lbw / bowled
        - players involved in the wicket
    '''
    wicket_str = wicket_str.rstrip().lstrip().lower().replace('†','')
    run_out = re.search(r'\(([a-z\s/-]+)\)', wicket_str)
    catch = re.search(r'c(?:\s*&\s*b)? (\w+)', wicket_str)
    lbw = re.search(r'lbw',wicket_str)
    bowled = re.search(r'b ([a-z\s-]+)',wicket_str)
    not_out = re.search(r'not\s+out',wicket_str)

    bowler = bowled.group(1) if bowled or lbw else ''

    if run_out:
        return True, 'run-out', [clean(name) for name in run_out.group(1).split('/')], bowler
    elif catch:
        return True, 'catch', [clean(catch.group(1))], bowler
    elif lbw:
        return True, 'lbw', [], bowler
    elif bowled:
        return True,'bowled', [], bowler
    elif not_out:
        return False, 'not-out', [], bowler
    else:
        print(f'Regex error - `{wicket_str}`')
        return True, '?', [], bowler

'''
Add ESPN cricinfo URL for a specific IPL season
'''
season_url = {
    2021: 'https://www.espncricinfo.com/series/ipl-2021-1249214/match-results',
    2020: 'https://www.espncricinfo.com/series/ipl-2020-21-1210595/match-results',
    2019: 'https://www.espncricinfo.com/series/ipl-2019-1165643/match-results',
    2018: 'https://www.espncricinfo.com/series/ipl-2018-1131611/match-results',
    2017: 'https://www.espncricinfo.com/series/ipl-2017-1078425/match-results',
}

'''Convert ordinal string to number (eg: 4th -> 4)'''
get_num = lambda x: int(''.join(c for c in x if c.isdigit()))


def find_closest_with_inn(name, curr_inn, squad):
    return find_closest(name, squad[1-curr_inn]['players'])

def find_closest(name, players):
    players = tuple(players)
    close = []
    close = [similar_name(name, player) for player in players]
    closest_match = max(close)
    inds = [i for i,c in enumerate(close) if c == closest_match]
    if len(inds) > 1 or closest_match < 0.45:
        return False, [players[i] for i in inds], closest_match
    else:
        return True, players[inds[0]], closest_match

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def similar_name(name1, name2):
    if len(name2.split('-')) < len(name1.split('-')):
        name2,name1 = name1,name2
    return sum([max(0.5*similar(ch1,ch2)+0.5*similar(ch2,ch1) for ch2 in name2.split('-')) for ch1 in name1.split('-')])/len(name1.split('-'))

''' alternate player names '''
with open('player_alt.json') as f:
    alt_players = json.load(f)

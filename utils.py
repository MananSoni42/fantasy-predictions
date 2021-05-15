import re
import json

clean = lambda s: s.lower().replace('(c)','').replace('†','').replace(u'\xa0', u' ').rstrip().lstrip().replace(' ','-')

get_toss_info = lambda toss: (clean(toss.split(',')[0]), 'bat' if 'bat' in toss.split() else 'bowl')

def get_wicket_info(wicket_str):
    wicket_str = wicket_str.rstrip().lstrip().lower().replace('†','')
    run_out = re.search(r'\(([a-z\s/]+)\)', wicket_str)
    catch = re.search(r'c(?:\s*&\s*b)? (\w+)', wicket_str)
    lbw = re.search(r'lbw',wicket_str)
    bowled = re.search(r'b ([a-z\s]+)',wicket_str)
    not_out = re.search(r'not\s+out',wicket_str)

    if run_out:
        return True, 'run-out', [clean(name) for name in run_out.group(1).split('/')]
    elif catch:
        return True, 'catch', [clean(catch.group(1))]
    elif lbw:
        return True, 'lbw', []
    elif bowled:
        return True,'bowled', []
    elif not_out:
        return False, 'not-out', []
    else:
        print(f'Regex error - `{wicket_str}`')
        return True, '?', []

season_url = {
    #2021: 'https://www.espncricinfo.com/series/ipl-2021-1249214/match-results',
    2020: 'https://www.espncricinfo.com/series/ipl-2020-21-1210595/match-results',
    #2019: 'https://www.espncricinfo.com/series/ipl-2019-1165643/match-results',
    #2018: 'https://www.espncricinfo.com/series/ipl-2018-1131611/match-results',
    #2017: 'https://www.espncricinfo.com/series/ipl-2017-1078425/match-results',
}

get_num = lambda x: int(''.join(c for c in x if c.isdigit()))

player_id = {
    'next-id': 1,
}

with open('player_alt.json') as f:
    alt_players = json.load(f)

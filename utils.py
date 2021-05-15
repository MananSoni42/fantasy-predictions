import re

clean = lambda s: s.lower().rstrip().lstrip().replace(u'\xa0', u' ').replace(' ','-')

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
        raise Exception(f'Error for str: `{wicket_str}`')

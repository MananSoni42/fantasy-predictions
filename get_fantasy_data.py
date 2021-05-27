import csv
from pprint import pprint
from utils import clean

def get_fantasy_points(row, role):
    '''
    Need to add
    - Bonnus for bowled / lbw
    - Bonus for run-out direct hit
    - Bonus for SR / ER
    '''

    points = 0
    # batting

    runs,out = int(row[3]), int(row[5])
    if role in ['bat', 'all'] and runs == 0 and out == 1:
        points -= 2
    else:
        fours, sixs = int(row[6]), int(row[7])
        points += runs + fours + 2*sixs

    if runs >= 100:
        points += 16
    elif runs >=50:
        points += 8
    elif runs >= 30:
        points += 4

    # bowling
    maiden, runs, wickets, econ = int(row[10]), int(row[11]), int (row[12]), float(row[13])
    points += 25*wickets + 12*maiden
    if wickets >=5:
        points += 16
    elif wickets >=4:
        points += 8
    elif wickets >=3:
        points += 4

    # fielding
    catches, runout, stumping = int(row[-3]), int(row[-2]), int(row[-1])
    points += 8*catches + 6*runout + 12*stumping
    if catches >= 3:
        points += 4

    # other

    return points

with open('final_data/data-match.csv') as f:
    data_matches = list(csv.reader(f))

with open('final_data/player_batting_record_backup.csv') as f:
    data_player = list(csv.reader(f))

header = [data_matches[0][0]] + ['wk', 'role'] + data_matches[0][1:] + ['points']
data_matches = data_matches[1:]
data_player = { clean(row[0]): [row[1],row[2]] for row in data_player[1:] }

#pprint(data_player)

with open('data-ipl-fantasy.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for row in data_matches:
        name = clean(row[0])
        if name in data_player:
            wk,role = data_player[name]
            writer.writerow([name,wk,role,*row[1:],get_fantasy_points(row,role)])

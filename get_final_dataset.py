import csv
import numpy as np
from pprint import pprint
from utils import clean
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

stadium_data = {}
with open('final_data/stadium_record.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        stadium_data[clean(row[0])] = [float(row[1]), float(row[9]), float(row[11])]

alltime_data = {}
with open('final_data/player_batting_record_backup.csv') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if clean(row [0]) in alltime_data:
            alltime_data[clean(row[0])][row[3]] = row
        else:
            alltime_data[clean(row[0])] = { row[3]: row }
alltime_header = [clean(h) for h in header]

ipl_data = {}
with open('final_data/data-ipl-fantasy.csv') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if clean(row[0]) in ipl_data:
            ipl_data[clean(row[0])].append(row)
        else:
            ipl_data[clean(row[0])] = [row]

ipl_header = [clean(h) for h in header]

for key,player in ipl_data.items():
    ipl_data[key] = sorted(player,
                    key=lambda x: (int(x[ipl_header.index('season')]),int(x[ipl_header.index('match')])),
                    reverse=True)

def get_alltime(player_name):
    formats = ['t20', 'fc', 'list-a']
    data = [0]*12

    int_ = lambda x: 0 if x == '-' else int(x)
    float_ = lambda x: 0 if x == '-' else float(x)

    for format in formats:
        row = alltime_data[player_name][format]
        if row[4] != '-':
            return [
                int_(row[alltime_header.index('runs-scored')]),
                float_(row[alltime_header.index('average')]),
                float_(row[alltime_header.index('strike-rate')]),
                int_(row[alltime_header.index('100s')]),
                int_(row[alltime_header.index('50s')]),
                int_(row[alltime_header.index('4s')]),
                int_(row[alltime_header.index('6s')]),
                int_(row[alltime_header.index('wkts')]),
                float_(row[alltime_header.index('ave')]),
                float_(row[alltime_header.index('econ')]),
                float_(row[alltime_header.index('sr')]),
                int_(row[alltime_header.index('catches')]) + int(row[alltime_header.index('stumpings')]),
            ]
    return data

def get_ipl_match(row):
    return np.array([
        int(row[ipl_header.index('batting-runs')]),
        float(row[ipl_header.index('out')]),
        float(row[ipl_header.index('balls')]),
        int(row[ipl_header.index('4s')]),
        int(row[ipl_header.index('6s')]),
        int(row[ipl_header.index('wickets')]),
        float(row[ipl_header.index('bowling-runs')]), # average
        float(row[ipl_header.index('overs')]), # econ
        float(0), # SR
        int(row[ipl_header.index('catches')]) + int(row[ipl_header.index('stumping')]),
        int(row[ipl_header.index('run-out')]) + int(row[ipl_header.index('run-out-direct')]),
        int(row[ipl_header.index('points')])
    ])

def get_ipl(player, season, match, num_innings):
    tmp_data = np.zeros((num_innings, 12))
    count = 0
    for row in ipl_data[player]:
        if count >= num_innings:
            break
        curr_season, curr_match = int(row[ipl_header.index('season')]), int(row[ipl_header.index('match')])
        if (curr_season,curr_match) < (season,match):
            tmp_data[count] = get_ipl_match(row)
            count += 1

    data = np.zeros(12)
    for i in [0,3,4,5,9,10,11]:
        #data[i] = np.sum([1/np.power(2,i) for i in reversed(range(num_innings))]*tmp_data[:,i])
        data[i] = np.sum(tmp_data[:,i])

    overs2balls = lambda x: -1 if np.isnan(x) else 6*int(x) + (10*x)%10
    nan = lambda x: -1 if np.isnan(x) or np.isinf(x) else x


    #data[1] = nan( np.sum([1/np.power(2,i) for i in reversed(range(num_innings))] * tmp_data[:,0]) / (np.sum(tmp_data[:,1])) ) # batting average
    data[1] = nan( np.sum(tmp_data[:,0]) / (np.sum(tmp_data[:,1])) ) # batting average
    data[2] = nan(100*np.sum(tmp_data[:,0]) / (np.sum(tmp_data[:,2]))) # batting SR
    data[6] = nan(np.sum(tmp_data[:,6]) / (np.sum(tmp_data[:,5]))) # bowling average
    data[7] = nan(np.sum(tmp_data[:,6]) / (np.sum(tmp_data[:,7]))) # bowling economy
    data[8] = nan(np.sum([overs2balls(x) for x in tmp_data[:,7]]) / (np.sum(tmp_data[:,5]))) # bowling SR

    for i in range(num_innings):
        tmp_data[i,1] = nan(tmp_data[i,0] / (tmp_data[i,1])) # batting average
        tmp_data[i,2] = nan(100*tmp_data[i,0] / (tmp_data[i,2])) # batting SR
        tmp_data[i,6] = nan(tmp_data[i,6] / (tmp_data[i,5])) # bowling average
        tmp_data[i,7] = nan(tmp_data[i,6] / (tmp_data[i,7])) # bowling economy
        tmp_data[i,8] = nan(overs2balls(tmp_data[i,7]) / (tmp_data[i,5])) # bowling SR

    return data, tmp_data

def get_row(player_name,season,match,num_innings=5):
    ipl_overall, ipl_individual = get_ipl(player_name,season,match,num_innings)
    alltime = get_alltime(player_name)
    data = np.zeros((num_innings+2, 12))
    data[0] = alltime
    data[1] = ipl_overall
    data[2:] = ipl_individual

    return [player_name] + list(data.flatten())

prefix = lambda p,x: [p.rstrip() + '-' + r for r in x]
innings = 10

base = [
    'runs-scored', 'average', 'strike-rate',
    '100s', '50s',
    '4s', '6s',
    'wkts', 'ave', 'econ', 'sr',
    'catches', 'run-outs', 'points'
]

header = ['player-name']
header += prefix('all-time',base[:-2])
header += prefix(f'ipl-last-n',base[:3]+base[5:])
for i in range(1,innings+1):
    header += prefix(f'ipl-{i}',base[:3]+base[5:])

header += [ 'Average Points', 'Average Batting-Runs', 'Average wicket per match',
            'Average sr', 'Average bowl econ', 'Matches played']
header += ['points']

ave_stats = dict()
binning = dict()

with open('final_data/ave_stats.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        ave_stats[clean(row[1])] = [row[2], row[3], row[4], row[5], row[6], row[7]]
pprint(ave_stats)

with open('final-data-v2.csv','w') as out_f:
    writer = csv.writer(out_f)
    writer.writerow(header)
    with open('final_data/data-ipl-fantasy.csv') as in_f:
        reader = csv.reader(in_f)
        next(reader)
        for row in reader:
            print(f'processing {row[:5]}')
            writer.writerow(get_row(clean(row[ipl_header.index('player-name')]),
                                         int(row[ipl_header.index('season')]),
                                         int(row[ipl_header.index('match')]), num_innings=innings) + ave_stats[row[ipl_header.index('player-name')]] + [int(row[ipl_header.index('points')])])
binny = pd.read_csv("final-data-v2.csv")
bins = [-14, 6, 22, 37, 62, 300]
labels = [1,2,3,4,5]
binny['binned-points'] = pd.cut(binny['points'], bins=bins, labels=labels)
binny.to_csv("final-data-v3.csv")
header2=['range1','range2','range3','range4','range5']
header2+=header
columnTransformer = ColumnTransformer([('encoder',
                                        OneHotEncoder(),
                                        [152])],
                                      remainder='passthrough')

binny = np.array(columnTransformer.fit_transform(binny), dtype = np.str)
pd.DataFrame(binny).to_csv("final-data-v4.csv",header=header2, index=None)

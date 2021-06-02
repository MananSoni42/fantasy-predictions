import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from pprint import pprint

other_path = "data-ipl-fantasy.csv"
df = pd.read_csv(other_path, header=None)
new_header = df.iloc[0]
df = df[1:]
df.columns = new_header
print(df.head(5))
clean = lambda x: x.replace(' ','').replace('\n','')
names=[]
names = set(df['player-name'])
names = set(list(names)[:5])

player_form = dict()
n = len(names)
for i,name in enumerate(names):
    print(f'{i+1}/{n}')
    hehe=[]
    #hehe0=[]
    hehe1=[]
    hehe2=[]
    hehe3=[]
    hehe4=[]

    for i in range(1,df.shape[0]+1):
        if(df.loc[i].at["player-name"]==name):
            #hehe0.append(df.loc[i].at["player-name"])
            hehe.append(df.loc[i].at["points"])
            hehe1.append(df.loc[i].at["batting-runs"])
            hehe2.append(df.loc[i].at["wickets"])
            hehe3.append(df.loc[i].at["sr"])
            hehe4.append(df.loc[i].at["econ"])
            #print(df.loc[i, ['player-name', 'points']])
    player_form[name] = pd.DataFrame(
        {'Points': hehe,
         'Batting-Runs': hehe1,
         'Wickets': hehe2,
         'Strike-Rate': hehe3,
         'Economy': hehe4,
         #'Player-name':hehe0
        })

pprint(player_form)

'''
player_form = player_form.astype(float)
print(player_form.dtypes)
#df['points'].value_counts()
player_form['Points'].apply(lambda x: float(x))
player_form['Batting-Runs'].apply(lambda x: float(x))
col1=player_form["Batting-Runs"]
col2=player_form["Points"]
correlation=col1.corr(col2)
print(correlation)
print(player_form.corr())
'''

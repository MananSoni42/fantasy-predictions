import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from pprint import pprint
import statistics
other_path = "data-ipl-fantasy.csv"
df = pd.read_csv(other_path, header=None)
new_header = df.iloc[0]
df = df[1:]
df.columns = new_header
convert_dict = { 'points':float,'batting-runs':float,'wickets':float,'sr':float,'econ':float}
df=df.astype(convert_dict)
#print(df.head(5))
clean = lambda x: x.replace(' ','').replace('\n','')
names=[]
names = set(df['player-name'])
names = set(list(names)[:5])

player_form = dict()
n = len(names)
lolmax=list()
count=list()
j=0
for i,name in enumerate(names):
    #print(f'{i+1}/{n}')
    hehe=[]
    hehe1=[]
    hehe2=[]
    hehe3=[]
    hehe4=[]
    c=0

    for i in range(1,df.shape[0]+1):
        if(df.loc[i].at["player-name"]==name):
            #hehe0.append(df.loc[i].at["player-name"])
            hehe.append(df.loc[i].at["points"])
            hehe1.append(df.loc[i].at["batting-runs"])
            hehe2.append(df.loc[i].at["wickets"])
            hehe3.append(df.loc[i].at["sr"])
            hehe4.append(df.loc[i].at["econ"])  
            c=c+1
    av1=statistics.mean(hehe)
    av2=statistics.mean(hehe1)
    av3=statistics.mean(hehe2)
    av4=statistics.mean(hehe3)
    av5=statistics.mean(hehe4)
    count.append(c)
    lolmax.append([name,av1,av2,av3,av4,av5,count[j]])  
    j=j+1
#print(player_form[axar-patel].groupby('batting').median())
lolmax=pd.DataFrame(lolmax)
lolmax.columns=["Player-name","Average Points","Average Batting-Runs","Average wicket per match","Average sr","Average bowl econ","Matches played"]
print(lolmax)


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

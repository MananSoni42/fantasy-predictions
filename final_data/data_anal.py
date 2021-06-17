import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from pprint import pprint
import statistics
import os
dir = 'plots'
if not os.path.exists(dir):
    os.mkdir(dir)
clean = lambda x: x.replace(' ','').replace('\n','')

#importing file and convrting it to PD dataframe
other_path = "data-ipl-fantasy.csv"
df = pd.read_csv(other_path, header=None)
new_header = df.iloc[0]
df = df[1:]
df.columns = new_header

#importing all time records nd converting it to dataframe

other_path = "final-data.csv"
df1 = pd.read_csv(other_path, header=None)
new_header1 = df1.iloc[0]
df1 = df1[1:]
df1.columns = new_header1

#list to store player-names for data analysis

convert_dict = { 'points':float,'batting-runs':float,'wickets':float,'sr':float,'econ':float,'balls':int}
df=df.astype(convert_dict)
names=[]
names = set(df['player-name'])
names = set(list(names)[:25])

#some variable initialization for future use

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
    cc=0
    for i in range(1,df.shape[0]+1):
        if(df.loc[i].at["player-name"]==name):
            #hehe0.append(df.loc[i].at["player-name"])
            if(df.loc[i].at["balls"]==0):
                cc=cc+1
            #print(df.loc[i].at["balls"])
            hehe.append(df.loc[i].at["points"])
            hehe1.append(df.loc[i].at["batting-runs"])
            hehe2.append(df.loc[i].at["wickets"])
            hehe3.append(df.loc[i].at["sr"])
            hehe4.append(df.loc[i].at["econ"])  
            c=c+1
    total=0
    print(c)
    print(cc)
    for ele in range(0, len(hehe3)):
        total = total + hehe3[ele]
    av1=statistics.mean(hehe)
    av2=statistics.mean(hehe1)
    av3=statistics.mean(hehe2)
    av4=total/(c-cc)
    av5=statistics.mean(hehe4)
    count.append(c)
    lolmax.append([name,av1,av2,av3,av4,av5,count[j]])  
    j=j+1
#print(player_form[axar-patel].groupby('batting').median())
lolmax=pd.DataFrame(lolmax)
lolmax.columns=["Player-name","Average Points","Average Batting-Runs","Average wicket per match","Average sr","Average bowl econ","Matches played"]
lolmax['Average sr'] = lolmax['Average sr'].fillna(0)
print(lolmax)

print(lolmax.corr())
stats_df=lolmax.describe()
stats_df.loc['range'] = stats_df.loc['max'] - stats_df.loc['min']
#stats_df
out_fields = ['mean','25%','50%','75%', 'range']
stats_df = stats_df.loc[out_fields]
#stats_df
stats_df.rename({'50%': 'median'}, inplace=True)
print(stats_df)

ax = lolmax.plot.hist(bins=25, alpha=0.5)
ax.set_xlabel('Size (cm)');
plt.savefig(os.path.join(dir,f'tp.png'))

lolu=lolmax.groupby('Matches played').mean()
print(lolu)

#sns.set_context('talk')
#sns.pairplot(lolmax, hue='Matches played');
#plt.savefig(os.path.join(dir,f'tps.png'))

sns.regplot(x="Average Points", y="Matches played", data=lolmax)
plt.savefig(os.path.join(dir,f'tpss.png'))

sns.regplot(x="Average Points", y="Matches played", data=lolmax)
plt.savefig(os.path.join(dir,f'tpsss.png'))
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

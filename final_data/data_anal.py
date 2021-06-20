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
df2 = df1.iloc[: , [0,13,14,15,16,17,18,19,20,21,22,23,24]].copy()
print(df2)
df1 = df1.iloc[:,:13]
print(df1)
#list to store player-names for data analysis

convert_dict = { 'points':float,'batting-runs':float,'wickets':float,'sr':float,'econ':float,'balls':int}
df=df.astype(convert_dict)
names=[]
names = set(df['player-name'])
names = set(list(names)[:150])


convert_dict_all_time = { 'all-time-runs-scored' : float, 'all-time-average' : float, 'all-time-strike-rate' : float, 'all-time-100s' : float, 'all-time-50s' : float, 'all-time-4s' : float, 'all-time-6s' : float, 'all-time-wkts' : float, 'all-time-ave' : float, 'all-time-econ' : float, 'all-time-sr' : float,'all-time-catches' : float}
df1=df1.astype(convert_dict_all_time)
names_at = set(df1['player-name'])
names_at = set(list(names)[:25])
#some variable initialization for future use

player_form = dict()
n = len(names)
gen_stats=list()
match_count=list()
j=0

for i,name in enumerate(names):
    #print(f'{i+1}/{n}')
    point=[]
    bat_run=[]
    wick=[]
    bat_strike_rate=[]
    bowl_econ=[]
    non_zero_balls_played=0
    zero_balls_played=0
    for i in range(1,df.shape[0]+1):
        if(df.loc[i].at["player-name"]==name):
            #hehe0.append(df.loc[i].at["player-name"])
            if(df.loc[i].at["balls"]==0):
                zero_balls_played=zero_balls_played+1
            #print(df.loc[i].at["balls"])
            point.append(df.loc[i].at["points"])
            bat_run.append(df.loc[i].at["batting-runs"])
            wick.append(df.loc[i].at["wickets"])
            bat_strike_rate.append(df.loc[i].at["sr"])
            bowl_econ.append(df.loc[i].at["econ"])  
            non_zero_balls_played=non_zero_balls_played+1
    total=0
    for ele in range(0, len(bat_strike_rate)):
        total = total + bat_strike_rate[ele]
    av1=statistics.mean(point)
    av2=statistics.mean(bat_run)
    av3=statistics.mean(wick)
    av4=total/(non_zero_balls_played-zero_balls_played)
    av5=statistics.mean(bowl_econ)
    match_count.append(non_zero_balls_played)
    gen_stats.append([name,av1,av2,av3,av4,av5,match_count[j]])  
    j=j+1
#print(player_form[axar-patel].groupby('batting').median())
gen_stats=pd.DataFrame(gen_stats)
gen_stats.columns=["Player-name","Average Points","Average Batting-Runs","Average wicket per match","Average sr","Average bowl econ","Matches played"]
gen_stats['Average sr'] = gen_stats['Average sr'].fillna(0)
print(gen_stats)

corr = gen_stats.corr()# plot the heatmap
sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, annot=True, cmap=sns.diverging_palette(220, 20, as_cmap=True))
plt.savefig(os.path.join(dir,f'heatmap.png'))

print(df1.corr())
print(df2.corr())

stats_df=gen_stats.describe()
stats_df.loc['range'] = stats_df.loc['max'] - stats_df.loc['min']
#stats_df
out_fields = ['mean','25%','50%','75%', 'range']
stats_df = stats_df.loc[out_fields]
#stats_df
stats_df.rename({'50%': 'median'}, inplace=True)
print(stats_df)

ax = gen_stats.plot.hist(bins=25, alpha=0.5)
ax.set_xlabel('Size (cm)');
plt.savefig(os.path.join(dir,f'tp.png'))

gen_stats_grouping=gen_stats.groupby('Matches played').mean()
print(gen_stats_grouping)

#sns.set_context('talk')
#sns.pairplot(lolmax, hue='Matches played');
#plt.savefig(os.path.join(dir,f'tps.png'))

sns.regplot(x="Average Points", y="Matches played", data=gen_stats)
plt.savefig(os.path.join(dir,f'tpss.png'))

sns.regplot(x="Average Points", y="Matches played", data=gen_stats)
plt.savefig(os.path.join(dir,f'tpsss.png'))

gen_stats.plot(kind='scatter', x='Average Points', y='Average Batting-Runs')
plt.savefig(os.path.join(dir,f'scatter.png'))

sns.pairplot(gen_stats)
plt.savefig(os.path.join(dir,f'pairplot.png'))
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

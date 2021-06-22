import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from pathlib import Path
from pprint import pprint
import statistics
import openpyxl
import xlsxwriter
import os
dir = 'plots'
if not os.path.exists(dir):
    os.mkdir(dir)
clean = lambda x: x.replace(' ','').replace('\n','')
data_dir = Path('..')

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
# copy the data
df_max_scaled = df1.copy()
df_min_max_scaled = df1.copy()
df_z_scaled = df1.copy()
df2 = df1.iloc[: , [0,13,14,15,16,17,18,19,20,21,22,23,24]].copy()
#print(df2)
df1 = df1.iloc[:,:13]
#print(df1)
#list to store player-names for data analysis

convert_dict = { 'points':float,'batting-runs':float,'wickets':float,'sr':float,'econ':float,'balls':int}
df=df.astype(convert_dict)
names=[]
names = set(df['player-name'])
names = set(list(names)[:25])


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

ave_stats=gen_stats.copy()

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



df_max_scaled.drop(columns=['player-name'],inplace=True)
df_max_scaled = df_max_scaled.apply(pd.to_numeric)  
# apply normalization techniques
for column in df_max_scaled.columns:
    df_max_scaled[column] = df_max_scaled[column]  / df_max_scaled[column].abs().max()
      
# view normalized data
print(df_max_scaled)

df_min_max_scaled.drop(columns=['player-name'],inplace=True)
df_min_max_scaled = df_min_max_scaled.apply(pd.to_numeric)
for column in df_min_max_scaled.columns:
    df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())
print(df_min_max_scaled)

  
# apply normalization techniques
df_z_scaled.drop(columns=['player-name'],inplace=True)
df_z_scaled = df_z_scaled.apply(pd.to_numeric)
for column in df_z_scaled.columns:
    df_z_scaled[column] = (df_z_scaled[column] -
                           df_z_scaled[column].mean()) / df_z_scaled[column].std()    
  
# view normalized data   
print(df_z_scaled)

names=df1['player-name']
df_max_scaled.insert(0,'player-name',names)
df_min_max_scaled.insert(0,'player-name',names)
df_z_scaled.insert(0,'player-name',names)

df_max_scaled.to_excel("mean_scaling.xlsx",sheet_name='mean_scaling')
df_min_max_scaled.to_excel("min_max_scaling.xlsx",sheet_name='min_max_scaling') 
df_z_scaled.to_excel("z_scaling.xlsx",sheet_name='z_scaling') 

#for gen_stats dataframe
names2=ave_stats['Player-name']
ave_stats.drop(columns=['Player-name'],inplace=True)
ave_stats = ave_stats.apply(pd.to_numeric)
ave_stats_z=ave_stats.copy()

for column in ave_stats.columns:
    ave_stats[column] = (ave_stats[column] - ave_stats[column].min()) / (ave_stats[column].max() - ave_stats[column].min())

for column in ave_stats_z.columns:
    ave_stats_z[column] = (ave_stats_z[column] -
                           ave_stats_z[column].mean()) / ave_stats_z[column].std()
ave_stats.insert(0,"Player-name",names2)
ave_stats_z.insert(0,"Player-name",names2)

ave_stats.to_excel("ave_stats_min_max_scaling.xlsx",sheet_name='min_max_scaling')
ave_stats_z.to_excel("ave_stats_z_scaling.xlsx",sheet_name='z_scaling')

#storing normalized data to dataframes and then splitting to test_train
ave_stats_mm = pd.read_excel('ave_stats_min_max_scaling.xlsx')
ave_stats_z = pd.read_excel('ave_stats_z_scaling.xlsx')
overall_ms=pd.read_excel('mean_scaling.xlsx')
overall_mm=pd.read_excel('min_max_scaling.xlsx')
overall_z=pd.read_excel('z_scaling.xlsx')

#splitting into train test_train
train_ave_mm, test_ave_mm = train_test_split(ave_stats_mm, test_size=0.2, random_state=42, shuffle=True)
train_ave_z, test_ave_z = train_test_split(ave_stats_z, test_size=0.2, random_state=42, shuffle=True)
train_overall_ms, test_overall_ms = train_test_split(overall_ms, test_size=0.2, random_state=42, shuffle=True)
train_overall_mm, test_overall_mm = train_test_split(overall_mm, test_size=0.2, random_state=42, shuffle=True)
train_overall_z, test_overall_z = train_test_split(overall_z, test_size=0.2, random_state=42, shuffle=True)

# determine the path where to save the train and test file
train_path = Path(data_dir, 'train_ave_mm.csv')
test_path = Path(data_dir, 'test_ave_mm.csv')

# save the train and test file
# again using the '\t' separator to create tab-separated-values files
train_ave_mm.to_csv(train_path, sep=',', index=False)
test_ave_mm.to_csv(test_path, sep=',', index=False)

train_path = Path(data_dir, 'train_ave_z.csv')
test_path = Path(data_dir, 'test_ave_z.csv')

# save the train and test file
# again using the '\t' separator to create tab-separated-values files
train_ave_z.to_csv(train_path, sep=',', index=False)
test_ave_z.to_csv(test_path, sep=',', index=False)

train_path = Path(data_dir, 'train_overall_ms.csv')
test_path = Path(data_dir, 'test_overall_ms.csv')

# save the train and test file
# again using the '\t' separator to create tab-separated-values files
train_overall_ms.to_csv(train_path, sep=',', index=False)
test_overall_ms.to_csv(test_path, sep=',', index=False)

train_path = Path(data_dir, 'train_overall_mm.csv')
test_path = Path(data_dir, 'test_overall_mm.csv')

# save the train and test file
# again using the '\t' separator to create tab-separated-values files
train_overall_mm.to_csv(train_path, sep=',', index=False)
test_overall_mm.to_csv(test_path, sep=',', index=False)

train_path = Path(data_dir, 'train_overall_z.csv')
test_path = Path(data_dir, 'test_overall_z.csv')

# save the train and test file
# again using the '\t' separator to create tab-separated-values files
train_overall_z.to_csv(train_path, sep=',', index=False)
test_overall_z.to_csv(test_path, sep=',', index=False)

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

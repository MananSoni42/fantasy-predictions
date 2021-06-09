import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

dir = 'plots'
if not os.path.exists(dir):
    os.mkdir(dir)

df = pd.read_csv('final_data/final-data-exp.csv', index_col='player-name')
df =df.replace(-1,np.nan)

# describe
print('--- Description ---')
print(df.describe())

# correlation

plt.clf()
sns.heatmap(df.corr())
plt.savefig(os.path.join(dir,'corr-all.png'))

corr_cols = ['all-time-runs-scored', 'all-time-average', 'all-time-strike-rate',
             'all-time-wkts', 'ipl-last-n-runs-scored', 'ipl-last-n-wkts', 'ipl-last-n-points',
             'ipl-1-points', 'ipl-2-points', 'ipl-3-points', 'ipl-4-points', 'ipl-5-points', 'points']

plt.clf()
sns.heatmap(df[corr_cols].corr())
plt.savefig(os.path.join(dir,'corr-some.png'))

print('--- Points correlation ---')
print(df.corr()['points'].sort_values(ascending=False))

# plots for each column
n = len(df.columns)
for i,col in enumerate(df.columns):
    print(f'Plotting {col} ({i+1}/{n})')
    plt.clf()
    sns.displot(x=df[col])
    plt.savefig(os.path.join(dir,f'{col}-hist.png'))


# violin plots comparing alltime to IPL

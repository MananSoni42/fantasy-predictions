import csv
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import KBinsDiscretizer
from math import floor,ceil
from tqdm import tqdm

df = pd.read_csv('final_data/final-data-v2.csv')
points = np.array(df['points']).reshape(-1,1)

dist = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='quantile')
dist.fit(points)

classes = dist.transform(points)
intervals = dist.bin_edges_[0].tolist()
intervals[0] = -14
intervals[-1] = 300

interval_map = [ (intervals[i], intervals[i+1]) for i in range(dist.n_bins_[0]) ]
print(interval_map)

num_runs = 30
n = classes.shape[0]

probs = np.zeros(300+14+1)
temp = 0.1
for i in range(n):
    probs[14+int(points[i][0])] += 1
probs_001 = np.exp(0.01*probs)
probs_01 = np.exp(0.05*probs)
probs_1 = np.exp(0.001*probs)

adaptive_probs = []
for i in range(len(interval_map)):
    lo,hi = interval_map[i]
    lo,hi = floor(lo), ceil(hi)
    adaptive_probs.append((
        lo,
        hi,
        probs_001[14+lo:hi+14+1]/np.sum(probs_001[14+lo:hi+14+1]),
        probs_01[14+lo:hi+14+1]/np.sum(probs_01[14+lo:hi+14+1]),
        probs_1[14+lo:hi+14+1]/np.sum(probs_1[14+lo:hi+14+1])
    ))

mean_points = np.zeros(n).reshape(-1,1)
uniform_points = np.zeros(num_runs*n).reshape(-1,1)
gaussian_points_3 = np.zeros(num_runs*n).reshape(-1,1)
gaussian_points_2 = np.zeros(num_runs*n).reshape(-1,1)
adaptive_points_001 = np.zeros(num_runs*n).reshape(-1,1)
adaptive_points_01 = np.zeros(num_runs*n).reshape(-1,1)
adaptive_points_1 = np.zeros(num_runs*n).reshape(-1,1)

for i in tqdm(range(num_runs*n)):
    ind = int(classes[i%n][0])
    lo,hi = interval_map[ind]
    lo1,hi1 = floor(lo), ceil(hi)
    mean, sd_3, sd_2 = (lo + hi) / 2, (hi - lo)/6, (hi-lo)/4

    mean_points[i%n] = round(0.5*lo + 0.5*hi)
    uniform_points[i] = np.random.randint(int(lo), int(hi))
    gaussian_points_3[i] = round(np.random.normal(loc=mean, scale=sd_3))
    gaussian_points_2[i] = round(np.random.normal(loc=mean, scale=sd_2))

    adaptive_points_001[i] = np.random.choice([i for i in range(lo1,hi1+1)], p=adaptive_probs[ind][2])
    adaptive_points_01[i] = np.random.choice([i for i in range(lo1,hi1+1)], p=adaptive_probs[ind][3])
    adaptive_points_1[i] = np.random.choice([i for i in range(lo1,hi1+1)], p=adaptive_probs[ind][4])

plt.subplot(421)
plt.title('Original')
sns.distplot(points, hist=False, color='r')
sns.distplot(points, kde=False, norm_hist=True, color='b')

plt.subplot(422)
plt.title('Mean')
sns.distplot(mean_points, hist=False, color='r')
sns.distplot(mean_points, kde=False, norm_hist=True, color='b')

plt.subplot(423)
plt.title('Random - uniform')
sns.distplot(uniform_points, hist=False, color='r')
sns.distplot(uniform_points, kde=False, norm_hist=True, color='b')

plt.subplot(424)
plt.title('Random - gaussian - 3sd')
sns.distplot(gaussian_points_3, hist=False, color='r')
sns.distplot(gaussian_points_3, kde=False, norm_hist=True, color='b')

plt.subplot(425)
plt.title('Random - gaussian - 2sd')
sns.distplot(gaussian_points_2, hist=False, color='r')
sns.distplot(gaussian_points_2, kde=False, norm_hist=True, color='b')

plt.subplot(426)
plt.title('Random - adaptive - 0.01')
sns.distplot(adaptive_points_001, hist=False, color='r')
sns.distplot(adaptive_points_001, kde=False, norm_hist=True, color='b')

plt.subplot(427)
plt.title('Random - adaptive - 0.05')
sns.distplot(adaptive_points_01, hist=False, color='r')
sns.distplot(adaptive_points_01, kde=False, norm_hist=True, color='b')

plt.subplot(428)
plt.title('Random - adaptive - 0.001')
sns.distplot(adaptive_points_1, hist=False, color='r')
sns.distplot(adaptive_points_1, kde=False, norm_hist=True, color='b')

plt.tight_layout()
plt.show()

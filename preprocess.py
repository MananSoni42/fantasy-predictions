from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

df = pd.read_csv('final-data-v3.csv')

y = df['binned-points']
x_mm = df.drop(columns=['points','binned-points'])
x_s= df.drop(columns=['points','binned-points'])

mm_scaler = MinMaxScaler()
s_scaler = StandardScaler()

x_mm.loc[:, x_mm.columns != 'player-name'] = mm_scaler.fit_transform(x_mm.loc[:, x_mm.columns != 'player-name'])
x_s.loc[:, x_s.columns != 'player-name'] = mm_scaler.transform(x_s.loc[:, x_s.columns != 'player-name'])


x_mm.to_csv('final-data-mm.csv')
x_s.to_csv('final-data-s.csv')

x_mm_train, x_mm_test, y_mm_train, y_mm_test = train_test_split(x_mm, y, test_size=0.2)
x_mm_eval, x_mm_test, y_mm_eval, y_mm_test = train_test_split(x_mm_test, y_mm_test, test_size=0.5)

x_s_train, x_s_test, y_s_train, y_s_test = train_test_split(x_s, y, test_size=0.2)
x_s_eval, x_s_test, y_s_eval, y_mstest = train_test_split(x_s_test, y_s_test, test_size=0.5)

x_mm_train.to_csv('x-train-mm.csv')
x_mm_eval.to_csv('x-eval-mm.csv')
x_mm_test.to_csv('x-test-mm.csv')
x_s_train.to_csv('x-train-s.csv')
x_s_eval.to_csv('x-eval-s.csv')
x_s_test.to_csv('x-test-s.csv')

y_mm_train.to_csv('y-train-mm.csv')
y_mm_eval.to_csv('y-eval-mm.csv')
y_mm_test.to_csv('y-test-mm.csv')
y_s_train.to_csv('y-train-s.csv')
y_s_eval.to_csv('y-eval-s.csv')
y_s_test.to_csv('y-test-s.csv')

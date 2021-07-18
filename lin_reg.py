import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import pandas as pd

data = pd.read_csv('final_data/final-data.csv')

test_rows = range(50)

y = data['points']
x = data.drop(['player-name', 'points'],axis=1)

x_test = x.iloc[test_rows]
y_test = y.iloc[test_rows]
x = x.drop(test_rows, axis=0)
y = y.drop(test_rows, axis=0)

reg = DecisionTreeRegressor().fit(x, y)

n = x.shape[0]

print('train results')
print(mean_squared_error(y, reg.predict(x)))

print('eval results')
print(mean_squared_error(y_test, reg.predict(x_test)))

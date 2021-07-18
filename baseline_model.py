import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRFRegressor
from lightgbm import LGBMRegressor

from sklearn.metrics import mean_squared_error, r2_score

x_train = pd.read_csv('final_data/x-train-s.csv')
y_train = pd.read_csv('final_data/y-train-s.csv')
x_eval = pd.read_csv('final_data/x-eval-s.csv')
y_eval = pd.read_csv('final_data/y-eval-s.csv')

x_train = x_train.drop(columns=['player-name', 'Unnamed: 0'])
x_eval = x_eval.drop(columns=['player-name', 'Unnamed: 0'])

y_train = np.array(y_train['points']).ravel()
y_eval = np.array(y_eval['points']).ravel()


models = {
	'linear regression': LinearRegression,
	'RBF SVM': SVR,
	'linear SVM': lambda: SVR(kernel='linear'),
	'poly SVM': lambda: SVR(kernel='poly'),
	'Decision Tree': lambda: DecisionTreeRegressor(max_depth=10),
	'ensemble-random-forest': RandomForestRegressor,
	'ensemble-xgb': XGBRFRegressor,
	'ensemble-lightgbm': LGBMRegressor,
}


print('x:', x_train.shape)
print('y:', y_train.shape)
print()

for name,model_func in models.items():
	print(name)
	model = model_func()
	model.fit(x_train,y_train)
	y_pred_train = model.predict(x_train)
	y_pred_eval = model.predict(x_eval)
	print('MSE(train): ', mean_squared_error(y_train, y_pred_train))
	print('MSE(eval): ', mean_squared_error(y_eval, y_pred_eval))
	print('R^2(train): ', r2_score(y_train, y_pred_train))
	print('R^2(eval): ', r2_score(y_eval, y_pred_eval))
	print()

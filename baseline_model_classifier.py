import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBRFClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense,Dropout

def label2onehot(arr):
	new_arr = np.zeros((arr.shape[0],5))
	for i in range(arr.shape[0]):
		new_arr[i][int(arr[i])] = 1
	return new_arr

def onehot2label(arr):
	new_arr = np.zeros(arr.shape[0])
	for i in range(arr.shape[0]):
		new_arr[i] = np.argmax(arr[i])
	return new_arr

x_train = pd.read_csv('final_data/x-train-s.csv')
y_train = pd.read_csv('final_data/y-train-s.csv')
x_eval = pd.read_csv('final_data/x-eval-s.csv')
y_eval = pd.read_csv('final_data/y-eval-s.csv')

x_train = x_train.drop(columns=['player-name', 'Unnamed: 0'])
x_eval = x_eval.drop(columns=['player-name', 'Unnamed: 0'])

y_train = (np.array(y_train['binned-points'])-1)
y_eval = (np.array(y_eval['binned-points'])-1)

y_train_onehot = label2onehot(y_train)
y_eval_onehot = label2onehot(y_eval)

models = {
	#'linear regression': LinearRegression,
	#'RBF SVM': SVR,
	#'linear SVM': lambda: SVR(kernel='linear'),
	#'poly SVM': lambda: SVR(kernel='poly'),
	#'Decision Tree': lambda: DecisionTreeClassifier(max_depth=10),
	#'ensemble-random-forest': RandomForestClassifier,
	#'ensemble-xgb': XGBRFClassifier,
	#'ensemble-lightgbm': LGBMClassifier,
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
	print('accuracy_score(train): ', accuracy_score(y_train, y_pred_train))
	print('accuracy_score(eval): ', accuracy_score(y_eval, y_pred_eval))
	print('classification_report(train): ', classification_report(y_train, y_pred_train))
	print('classification_report(eval): ', classification_report(y_eval, y_pred_eval))
	print()

#neural_network
def create_baseline():
	# create model
	model = Sequential()
	model.add(Dense(200, input_dim=151, activation='relu'))
	model.add(Dropout(0.3))
	model.add(Dense(100, activation='relu'))
	model.add(Dropout(0.2))
	model.add(Dense(5, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

model = create_baseline()
model.fit(x_train,y_train_onehot,epochs=100,batch_size=128)
y_pred_train = onehot2label(model.predict(x_train))
y_pred_eval = onehot2label(model.predict(x_eval))

print(y_pred_train[:10])
print(y_train[:10])

print('accuracy_score(train): ', accuracy_score(y_train, y_pred_train))
print('accuracy_score(eval): ', accuracy_score(y_eval, y_pred_eval))
print('classification_report(train):\n', classification_report(y_train, y_pred_train))
print('classification_report(eval):\n', classification_report(y_eval, y_pred_eval))
print()

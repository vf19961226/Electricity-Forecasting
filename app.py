# -*- coding: utf-8 -*-
"""

"""

import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM, TimeDistributed
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("--data",default="./data/training_data.csv",help="Input your training data.")
parser.add_argument("--output",default="submission.csv",help="Output your predict data.")
args=parser.parse_args()

#匯入資料集
train_data = pd.read_csv(args.data)
#讀取前20條data
train_data.head(20)

def readTrain():
  train = pd.read_csv(args.data)
  return train

#正規化
def normalize(train):
  train_norm = train.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
  return train_norm

#建立訓練data
def buildTrain(train,pastDay=30,futureDay=8):
    X_train, Y_train = [], []
    for i in range(train.shape[0]-futureDay-pastDay):
      X_train.append(np.array(train.iloc[i:i+pastDay]))
      Y_train.append(np.array(train.iloc[i+pastDay:i+pastDay+futureDay]["Operating Reserve"]))
    return np.array(X_train), np.array(Y_train)
#分割data
def splitData(X,Y,rate):
  X_train = X[int(X.shape[0]*rate):]
  Y_train = Y[int(Y.shape[0]*rate):]
  X_val = X[:int(X.shape[0]*rate)]
  Y_val = Y[:int(Y.shape[0]*rate)]
  return X_train, Y_train, X_val, Y_val

# read SPY.csv
train = readTrain()

# Normalization
train_norm = normalize(train)

# build Data, use last 30 days to predict next 5 days
X_train, Y_train = buildTrain(train_norm, 30, 8)

# split training data and validation data
X_train, Y_train, X_val, Y_val = splitData(X_train, Y_train, 0.1)

def buildManyToManyModel(shape):
  model = Sequential()
  
  model.add(LSTM(4, input_length=shape[1], input_dim=shape[2], return_sequences=True))
  # output shape: (7, 1)
  model.add(TimeDistributed(Dense(1)))
  model.compile(loss="mse", optimizer="Adam")
  model.summary()
  return model

train = readTrain()

train_norm = normalize(train)
# change the last day and next day 
X_train, Y_train = buildTrain(train_norm,8, 8)

X_train, Y_train, X_val, Y_val = splitData(X_train, Y_train, 0.1)

model = buildManyToManyModel(X_train.shape)
callback = EarlyStopping(monitor="loss", patience=10, verbose=1, mode="auto")

Y_train=np.reshape(Y_train,(Y_train.shape[0],Y_train.shape[1],1))
Y_val=np.reshape(Y_val,(Y_val.shape[0],Y_val.shape[1],1))
history=model.fit(X_train, Y_train, epochs=1000, batch_size=128, validation_data=(X_val, Y_val), callbacks=[callback])

fig = plt.figure()
plt.plot(history.history['loss'],label='training loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(loc='upper right')
fig.savefig("./figure/power_prediction.png")

model.save('./power_prediction.h5')

from tensorflow.keras.models import load_model
model = load_model('./power_prediction.h5') 

predict_data = pd.read_csv(args.data)

#正規化
def normalize(train):
  train_norm = train.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
  return train_norm

#建立訓練data
def buildTrain(train,pastDay=8,futureDay=8):
    X_predict = []
    for i in range(predict_data.shape[0]-futureDay-pastDay):
      X_predict.append(np.array(train.iloc[i:i+pastDay]))
    return np.array(X_predict)



# Normalization
predict_norm = normalize(predict_data)

# build Data, use last 30 days to predict next 5 days
X_predict = buildTrain(predict_norm, 8, 8)
print(X_predict.shape)
print(X_predict)

predict = model.predict(X_predict)
predict_reshape=np.reshape(predict,(predict.shape[0],predict.shape[1]))
sub=predict_reshape[-1]
dfs= pd.DataFrame(sub)
denorm = dfs.apply(lambda x: x*(np.max(predict_data['Operating Reserve'])-np.min(predict_data['Operating Reserve']))+np.mean(predict_data['Operating Reserve']))
dfs_print = denorm
#print(dfs_print)
dfs_print.drop([0],inplace=True)
new1=dfs_print.rename({1:20200323,2:20200324,3:20200325,4:20200326,5:20200327,6:20200328,7:20200329},axis='index')
print(new1)
new1.to_csv(args.output)

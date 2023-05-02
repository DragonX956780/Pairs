import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler

def calculate_indicators(data):
    # Bollinger Bands
    data['SMA'] = data['Close'].rolling(window=20).mean()
    data['StdDev'] = data['Close'].rolling(window=20).std()
    data['UpperBB'] = data['SMA'] + (2 * data['StdDev'])
    data['LowerBB'] = data['SMA'] - (2 * data['StdDev'])

    # RSI
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Moving Averages
    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['SMA200'] = data['Close'].rolling(window=200).mean()

    return data

def create_dataset(data, lookback=10):
    X, y = [], []
    for i in range(lookback, len(data)):
        X.append(data[i-lookback:i])
        y.append(data[i][-1])
    return np.array(X), np.array(y)

def create_nn_model(input_dim):
    model = Sequential()
    model.add(Dense(128, input_dim=input_dim, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])
    return model

def train_nn_strategy(stock_data, pairs_result):
    stock_data['NNInput'] = pairs_result
    data = calculate_indicators(stock_data)
    data = data.dropna()

    input_features = ['UpperBB', 'LowerBB', 'Volume', 'RSI', 'SMA50', 'SMA200', 'NNInput']
    data = data[input_features]

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    lookback = 10
    X, y = create_dataset(scaled_data, lookback)

    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    input_dim = X_train.shape[1] * X_train.shape[2]
    X_train = X_train.reshape(-1, input_dim)
    X_test = X_test.reshape(-1, input_dim)

    model = create_nn_model(input_dim)
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

    return model, scaler, lookback

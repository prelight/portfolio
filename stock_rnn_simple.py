import copy
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import SimpleRNN
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle


EXCEL_BOOK = '1321-from2001.xlsx'
EXCEL_SHEET = '1321-from2001'


def load_candles():
    #excelから株価(ローソク足)取得
    excel = pd.ExcelFile(EXCEL_BOOK)
    for sheet in excel.sheet_names:
        if sheet == EXCEL_SHEET :
            candles = excel.parse(sheet, header=None)

    #column名、定義(時間、始値、高値、安値、終値、出来高)
    candles.columns = ["time", "open", "high", "low", "close", "volume"]

    #正規化
    candles = candles.sort_values(by=['time'], ascending=True)#index 0が一番古い
    candles['n_close'] = candles['close'] / candles['close'].max()

    return candles


def make_train_data(x, y):
    n_all = len(x)

    #訓練データ(仮)、テストデータ取得
    n_train_tmp = int(n_all * 0.9)
    n_test = n_all - n_train_tmp
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=n_test, shuffle=False)

    #訓練データ、検証データ取得
    n_train = int(n_train_tmp * 0.9)
    n_validation = n_train_tmp - n_train
    x_train, x_validation, y_train, y_validation = train_test_split(x_train, y_train, test_size=n_validation)

    return x_train, x_validation, x_test, y_train, y_validation, y_test


def weight_variable(shape, name=None):
    return np.random.normal(scale=.01, size=shape)


def write_data(_data, _filename):
    ff = open(_filename, 'w')
    writer = csv.writer(ff, lineterminator='\n')
    if np.array(_data).ndim == 1:
        writer.writerow(_data)
    else:
        writer.writerows(_data)

    ff.close()


def make_learning_data(candles, maxlen):
    src_prices = [] #予測する為の元となる株価(配列の配列)
    act_prices = [] #予測と比較する為の実際の株価(配列)
    for i in range(0, len(candles) - maxlen):
        src_prices.append(candles['n_close'].data[i: i + maxlen])
        act_prices.append(candles['n_close'].data[i + maxlen])

    #write_data(src_prices, 'some1.csv')
    #write_data(act_prices, 'some2.csv')

    #reshapeして整形
    n_all = len(src_prices)
    x = np.array(src_prices).reshape(n_all, maxlen, 1)
    y = np.array(act_prices).reshape(n_all, 1)
    return x, y


def create_model(x, y, maxlen):
    n_in = len(x[0][0])  # 1
    n_hidden = 30
    n_out = len(y[0])  # 1

    model = Sequential()
    model.add(SimpleRNN(n_hidden,
                        kernel_initializer=weight_variable,
                        input_shape=(maxlen, n_in)))
    model.add(Dense(n_out, kernel_initializer=weight_variable))
    model.add(Activation('linear'))

    optimizer = Adam(lr=0.001, beta_1=0.9, beta_2=0.999)
    model.compile(loss='mean_squared_error',
                  optimizer=optimizer,
                  metrics=['accuracy'])
    return model


def make_predicted(model, x_test):
    predicted = []
    n_test = len(x_test)
    for i in range(n_test):
        data = x_test[i:i+1]
        pred = model.predict(data)
        predicted.append(pred.reshape(-1))
    return predicted


def draw_graph(predicted, y_test):
    plt.rc('font', family='serif')
    plt.figure()
    plt.ylim([0.5, 1.0])
    plt.plot(y_test, linestyle='dashed', color='red')#実際の値
    plt.plot(predicted, color='black')#予測値
    plt.show()



def main():
    #株価(ローソク足)取得
    candles = load_candles()

    #学習用元データ取得
    maxlen = 10 #過去10日間
    x, y = make_learning_data(candles, maxlen)

    #訓練データ、検証データ、テストデータ取得
    x_train, x_validation, x_test, y_train, y_validation, y_test = make_train_data(x, y)

    #モデル設定
    model = create_model(x, y, maxlen)

    #モデル学習
    epochs = 30
    batch_size = 10
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1)
    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=(x_validation, y_validation),
              callbacks=[early_stopping])

    #予測値取得
    predicted = make_predicted(model, x_test)

    #グラフで可視化
    draw_graph(predicted, y_test)


if __name__ == '__main__':
    main()

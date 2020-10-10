import os
import sys
import json
import tensorflow.keras as kr
import tensorflow.keras.preprocessing.text as kpt
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pandas as pd
from tensorflow.keras.callbacks import EarlyStopping
import pickle


def main():
    if not os.path.exists(os.getcwd() + '/model/'):
        os.mkdir(os.getcwd() + '/model/')
    if not os.path.exists(os.getcwd() + '/model/email_classifier'):
        os.mkdir(os.getcwd() + '/model/email_classifier')
    df = pd.read_csv(os.getcwd() + '/data/cnn_model_training_data.txt')
    df.columns = ["label", "feature"]
    x = df['feature'].values
    y = df['label'].values
    max_words = 3000

    #x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

    tokenizer = Tokenizer(max_words)
    tokenizer.fit_on_texts(x)
    with open(os.getcwd() + '/model/email_classifier/tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #xtrain = tokenizer.texts_to_sequences(x_train)
    #xtest = tokenizer.texts_to_sequences(x_test)
    x = tokenizer.texts_to_sequences(x)

    vocab_size = len(tokenizer.word_index) + 1
    print(vocab_size)

    maxlen = 5
    #xtrain = pad_sequences(xtrain, padding='post', maxlen=maxlen)
    #xtest = pad_sequences(xtest, padding='post', maxlen=maxlen)
    x = pad_sequences(x, padding='post', maxlen=maxlen)

    #print(x_train[3])
    #print(xtrain[3])
    print(x[3])

    embedding_dim = 100
    model = Sequential()

    model.add(layers.Embedding(input_dim=vocab_size,
                               output_dim=embedding_dim,
                               input_length=maxlen))
    model.add(layers.LSTM(units=100, return_sequences=True))
    model.add(layers.LSTM(units=20))
    model.add(layers.Dropout(0.1))
    model.add(layers.Dense(8))
    model.add(layers.Dense(5, activation="sigmoid"))

    '''
    model.add(layers.Embedding(input_dim=vocab_size,
                               output_dim=embedding_dim,
                               input_length=maxlen))
    model.add(layers.SpatialDropout1D(0.2))
    model.add(layers.LSTM(100, dropout=0.2, recurrent_dropout=0.2))
    model.add(layers.Dense(3, activation='softmax'))
    '''

    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=['accuracy'])
    model.summary()
    #model.fit(xtrain, y_train, epochs=50, batch_size=200, verbose=True, shuffle=True, callbacks=[EarlyStopping(monitor='loss', patience=5, min_delta=0.0001)])
    #model.fit(xtrain, y_train, epochs=50, batch_size=200, verbose=True, shuffle=True)
    model.fit(x, y, epochs=30, batch_size=100, verbose=True, shuffle=True)

    model_json = model.to_json()
    with open(os.getcwd() + '/model/email_classifier/model.json', 'w') as json_file:
        json_file.write(model_json)

    model.save_weights(os.getcwd() + '/model/email_classifier/model.h5')

    print('saved model!')

    #loss, acc = model.evaluate(xtrain, y_train, verbose=True)
    loss, acc = model.evaluate(x, y, verbose=True)
    print("Training Accuracy: ", acc.round(2))
    #loss, acc = model.evaluate(xtest, y_test, verbose=True)
    #print("Test Accuracy: ", acc.round(2))
    #print(xtest)

    #ypred = model.predict(xtest)
    #print('pred:', ypred)

    #cm = confusion_matrix(y_test, ypred)
    #print(cm)


if __name__ == "__main__":
    main()

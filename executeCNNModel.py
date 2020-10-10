import os
import re
import json
import sys
import mysql.connector
import numpy as np
import tensorflow
import tensorflow.keras.preprocessing.text as kpt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import model_from_json
from nltk.corpus import stopwords
from nltk.corpus import wordnet

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import layers
import pickle


class executeCNNModel:
    def __init__(self):
        return

    def execute(self, testData):
        with open(os.getcwd() + '/model/email_classifier/tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        # read in your saved model structure
        json_file = open(os.getcwd() + '/model/email_classifier/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        # and create a model from that
        model = model_from_json(loaded_model_json)
        # and weight your nodes with your saved values
        model.load_weights(os.getcwd() + '/model/email_classifier/model.h5')
        labels = ['unknown_template', 'status_template', 'track_template', 'cancel_template', 'complain_template']
        prediction = 0
        xtest = tokenizer.texts_to_sequences([testData])
        #print('testDataSequence:', xtest)

        maxlen = 5
        xtest = pad_sequences(xtest, padding='post', maxlen=maxlen)
        #print(tokenizer.word_index)

        # predict which bucket your input belongs in
        pred = model.predict(xtest)
        # and print it for the humons
        #print(testData, 'pred:', pred)
        print("%s sentiment; %f%% confidence" % (labels[np.argmax(pred)], pred[0][np.argmax(pred)] * 100))
        #print('matches:', np.argmax(pred))
        return np.argmax(pred), pred[0][np.argmax(pred)] * 100


'''
executeCNNModel().execute("trakid none order track") #track_template
executeCNNModel().execute("trakid none deliveri day") #track_template
executeCNNModel().execute("trakid none track thank") #track_template
executeCNNModel().execute("trakid none week ship") #track_template
executeCNNModel().execute("none odderid intelegencia www")  #status_template
executeCNNModel().execute("none odderid order statu")  #status_template
executeCNNModel().execute("none odderid regard order")  #status_template
executeCNNModel().execute("none odderid statu order")  #status_template
executeCNNModel().execute("trakid odderid intelegencia www") #track_template
executeCNNModel().execute("trakid odderid order statu") #track_template
executeCNNModel().execute("trakid odderid regard order") #track_template
executeCNNModel().execute("trakid odderid statu order") #track_template
executeCNNModel().execute("none none order statu") #unknown_template
executeCNNModel().execute("none none deliveri day") #unknown_template
executeCNNModel().execute("none none track thank") #unknown_template
executeCNNModel().execute("none none week ship") #unknown_template
executeCNNModel().execute("none odderid ship week") #track_template
executeCNNModel().execute("none odderid deliveri time") #track_template
executeCNNModel().execute("none odderid day ship") #track_template
executeCNNModel().execute("none odderid day track") #track_template
executeCNNModel().execute("none odderid accept cancel") #cancel_template
executeCNNModel().execute("none odderid refund time") #cancel_template
executeCNNModel().execute("none odderid day return") #cancel_template
executeCNNModel().execute("none odderid cancel track") #cancel_template
executeCNNModel().execute("none odderid accept complain") #complain_template
executeCNNModel().execute("none odderid replac www") #complain_template
executeCNNModel().execute("none odderid damag item") #complain_template
executeCNNModel().execute("none odderid issu product") #complain_template
'''
'''
executeCNNModel().execute("trakid none track") #track_template
executeCNNModel().execute("trakid none deliveri") #track_template
executeCNNModel().execute("trakid none track") #track_template
executeCNNModel().execute("trakid none ship") #track_template
executeCNNModel().execute("none odderid www")  #status_template
executeCNNModel().execute("none odderid order")  #status_template
executeCNNModel().execute("none odderid regard")  #status_template
executeCNNModel().execute("none odderid statu")  #status_template
'''
'''
    def connectdb():
        connection = mysql.connector.connect(
            host="138.68.180.92",
            user="ayurai",
            passwd="ayura!DB@123",
            database="ayuraidb"
        )
        return connection


    def closedb(connection):
        connection.close()


    def rollbackdb(connection):
        connection.rollback()
'''


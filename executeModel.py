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


class executeModel:
    def __init__(self):
        return

    def convert_text_to_index_array(text, dictionary):
        words = kpt.text_to_word_sequence(text)
        wordIndices = []
        for word in words:
            if word in dictionary:
                wordIndices.append(dictionary[word])
            else:
                print("'%s' not in training corpus; ignoring." % word)
        return wordIndices

    def execute(self, testData):
        tokenizer = Tokenizer(num_words=3000)

        with open(os.getcwd() + '/model/email_classifier/dictionary.json', 'r') as dictionary_file:
            dictionary = json.load(dictionary_file)
        # read in your saved model structure
        json_file = open(os.getcwd() + '/model/email_classifier/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        # and create a model from that
        model = model_from_json(loaded_model_json)
        # and weight your nodes with your saved values
        model.load_weights(os.getcwd() + '/model/email_classifier/model.h5')
        labels = ['unknown_template', 'status_template', 'track_template']
        prediction = 0
        testArr1 = executeModel.convert_text_to_index_array(testData[0], dictionary)
        testArr2 = executeModel.convert_text_to_index_array(testData[1], dictionary)
        testArr3 = executeModel.convert_text_to_index_array(testData[2], dictionary)
        testArr4 = executeModel.convert_text_to_index_array(testData[3], dictionary)
        #print('testArr:', testArr1)
        #print('testArr:', testArr2)
        #print('testArr:', testArr3)
        #print('testArr:', testArr4)
        input1 = tokenizer.sequences_to_matrix([testArr1], mode='binary')
        input2 = tokenizer.sequences_to_matrix([testArr2], mode='binary')
        input3 = tokenizer.sequences_to_matrix([testArr3], mode='binary')
        input4 = tokenizer.sequences_to_matrix([testArr4], mode='binary')
        #print('input1:', input1)
        #print('input2:', input2)
        #print('input3:', input3)
        #print('input4:', input4)
        # predict which bucket your input belongs in
        pred = model.predict([input1, input2, input3, input4])
        print('pred:', pred)
        # and print it for the humons
        print("%s sentiment; %f%% confidence" % (labels[np.argmax(pred)], pred[0][np.argmax(pred)] * 100))
        print('matches:', np.argmax(pred))
        return np.argmax(pred)


executeModel().execute(['none', 'odderid', 'order', 'statu'])
executeModel().execute(['none', 'odderid', 'deliveri', 'day'])
executeModel().execute(['none', 'odderid', 'track', 'thank'])
executeModel().execute(['none', 'odderid', 'week', 'ship'])
executeModel().execute(['none', 'none', 'order', 'statu'])
executeModel().execute(['none', 'none', 'deliveri', 'day'])
executeModel().execute(['none', 'none', 'track', 'thank'])
executeModel().execute(['none', 'none', 'week', 'ship'])
executeModel().execute(['trakid', 'none', 'order', 'statu'])
executeModel().execute(['trakid', 'none', 'deliveri', 'day'])
executeModel().execute(['trakid', 'none', 'track', 'thank'])
executeModel().execute(['trakid', 'none', 'week', 'ship'])

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


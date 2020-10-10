import os
import sys
import json
import tensorflow.keras as kr
import tensorflow.keras.preprocessing.text as kpt
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout


def convert_text_to_index_array(text, dictionary):
    return [dictionary[word] for word in kpt.text_to_word_sequence(text)]


def main():
    if not os.path.exists(os.getcwd() + '/model/'):
        os.mkdir(os.getcwd() + '/model/')
    if not os.path.exists(os.getcwd() + '/model/email_classifier'):
        os.mkdir(os.getcwd() + '/model/email_classifier')
    training = np.genfromtxt(os.getcwd() + '/data/dnn_model_training_data.txt', delimiter=',', skip_header=1,
                             usecols=(0, 1, 2, 3, 4), dtype=None, encoding='utf-8')

    feature = [[str(x[1]), str(x[2]), str(x[3]), str(x[4])] for x in training]
    # index all the sentiment labels
    label = np.asarray([x[0] for x in training])

    # only work with the 3000 most popular words found in our dataset
    max_words = 3000

    # create a new Tokenizer
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(feature)

    dictionary = tokenizer.word_index
    with open(os.getcwd() + '/model/email_classifier/dictionary.json', 'w') as dictionary_file:
        json.dump(dictionary, dictionary_file)

    wordIndicesList1 = []
    wordIndicesList2 = []
    wordIndicesList3 = []
    wordIndicesList4 = []
    for featurerow in feature:
        #print(featurerow[0], featurerow[1], featurerow[2], featurerow[3])
        wordIndices1 = convert_text_to_index_array(featurerow[0], dictionary)
        wordIndices2 = convert_text_to_index_array(featurerow[1], dictionary)
        wordIndices3 = convert_text_to_index_array(featurerow[2], dictionary)
        wordIndices4 = convert_text_to_index_array(featurerow[3], dictionary)
        wordIndicesList1.append(wordIndices1)
        wordIndicesList2.append(wordIndices2)
        wordIndicesList3.append(wordIndices3)
        wordIndicesList4.append(wordIndices4)

    wordIndicesList1 = np.asarray(wordIndicesList1)
    wordIndicesList2 = np.asarray(wordIndicesList2)
    wordIndicesList3 = np.asarray(wordIndicesList3)
    wordIndicesList4 = np.asarray(wordIndicesList4)

    feature1 = tokenizer.sequences_to_matrix(wordIndicesList1, mode='binary')
    feature2 = tokenizer.sequences_to_matrix(wordIndicesList2, mode='binary')
    feature3 = tokenizer.sequences_to_matrix(wordIndicesList3, mode='binary')
    feature4 = tokenizer.sequences_to_matrix(wordIndicesList4, mode='binary')

    label = kr.utils.to_categorical(label, 3)

    model = Sequential()
    model.add(Dense(512, input_shape=(max_words,), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(256, activation='sigmoid'))
    model.add(Dropout(0.5))
    model.add(Dense(3, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    model.fit(x=[feature1, feature2, feature3, feature4], y=label,
              batch_size=200,
              epochs=5,
              verbose=1,
              validation_split=0.2,
              shuffle=True)

    model_json = model.to_json()
    with open(os.getcwd() + '/model/email_classifier/model.json', 'w') as json_file:
        json_file.write(model_json)

    model.save_weights(os.getcwd() + '/model/email_classifier/model.h5')

    print('saved model!')


if __name__ == "__main__":
    main()
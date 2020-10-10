import os
import numpy as np
import pickle
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from num2words import num2words
from sklearn.feature_extraction.text import TfidfVectorizer

stemmer = SnowballStemmer("english")


def convert_lower_case(data):
    return np.char.lower(data)


def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text


def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data


def remove_apostrophe(data):
    return np.char.replace(data, "'", "")


def stemming(data):
    #stemmer = PorterStemmer()
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text


def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text


def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data) #remove comma seperately
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
#    data = convert_numbers(data)
    data = stemming(data)
    data = remove_punctuation(data)
#    data = convert_numbers(data)
    data = stemming(data) #needed again as we need to stem the words
    data = remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
    data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
    return data


processed_text = []
entries = os.scandir(os.getcwd() + '/data/trainingdata/')
N = 0

for i in entries:
    N = N + 1
#    print(N)
#    file = open(i[0], 'r', encoding="utf8", errors='ignore')
    file = open(os.getcwd() + '/data/trainingdata/' + i.name, 'r', encoding="utf8", errors='ignore')
    text = file.read().strip()
    file.close()
#    print(text)
    allOrderId = re.findall(r'WS\d+|ws\d+|\d+\-\d+\-\d+', text)
    if len(allOrderId) > 0:
        orderId = allOrderId[0]
#        print(orderId)
        content_text = re.sub(r'WS\d+|ws\d+|\d+\-\d+\-\d+', "", text)
        content_text = str(preprocess(content_text))
#        print(content_text)
        content_text = word_tokenize(content_text)
#        print(content_text)
        processed_text.append(content_text)

#print("processed_text:" + str(processed_text))

new_processed_text = []
for item in processed_text:
    itemStr = str(item)
    itemStr = itemStr.replace('\'', '')
    itemStr = itemStr.replace(',', '')
    itemStr = itemStr.replace('[', '')
    itemStr = itemStr.replace(']', '')
#    print("itemStr:" +itemStr)
    new_processed_text.append(itemStr)

#print(new_processed_text)

# tf-idf based vectors
tf = TfidfVectorizer(analyzer='word', ngram_range=(1,1), stop_words="english", max_features=500000)

# Fit the model
tf_transformer = tf.fit(new_processed_text)
print(tf_transformer.vocabulary_)
#print(tf_transformer.idf_)

# Dump the file
pickle.dump(tf_transformer, open("model/email_tf_idf/tfidf1.pkl", "wb"))

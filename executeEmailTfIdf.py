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


class executeEmailTfIdf:
    def __init__(self):
        return

    # Testing phase
    tf1 = pickle.load(open("model/email_tf_idf/tfidf1.pkl", 'rb'))

    # Create new tfidfVectorizer with old vocabulary
    tf1_new = TfidfVectorizer(analyzer='word', ngram_range=(1,1), stop_words = "english", lowercase = True,
                              max_features = 500000, vocabulary = tf1.vocabulary_)


    def print_doc(id):
        print(dataset[id])
        file = open(dataset[id][0], 'r', encoding='cp1250')
        text = file.read().strip()
        file.close()
        #print(text)

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
        data = executeEmailTfIdf.convert_lower_case(data)
        data = executeEmailTfIdf.remove_punctuation(data) #remove comma seperately
        data = executeEmailTfIdf.remove_apostrophe(data)
        data = executeEmailTfIdf.remove_stop_words(data)
    #    data = executeEmailTfIdf.convert_numbers(data)
        data = executeEmailTfIdf.stemming(data)
        data = executeEmailTfIdf.remove_punctuation(data)
    #    data = executeEmailTfIdf.convert_numbers(data)
        data = executeEmailTfIdf.stemming(data) #needed again as we need to stem the words
        data = executeEmailTfIdf.remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
        data = executeEmailTfIdf.remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
        return data

    def sort_coo(coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    def extract_topn_from_vector(feature_names, sorted_items, topn=10):
        """get the feature names and tf-idf score of top n items"""

        # use only topn items from vector
        sorted_items = sorted_items[:topn]

        score_vals = []
        feature_vals = []

        for idx, score in sorted_items:
            fname = feature_names[idx]

            # keep track of feature name and its corresponding score
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

        # create a tuples of feature,score
        # results = zip(feature_vals,score_vals)
        results = {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]] = score_vals[idx]

        return results

    def apply_tfidf(orderId, processed_text):
        new_processed_text = []
        for item in processed_text:
            itemStr = str(item)
            itemStr = itemStr.replace('\'', '')
            itemStr = itemStr.replace(',', '')
            itemStr = itemStr.replace('[', '')
            itemStr = itemStr.replace(']', '')
        #    print("itemStr:" +itemStr)
            new_processed_text.append(itemStr)

    #    print(new_processed_text)

        X_tf1 = executeEmailTfIdf.tf1_new.fit_transform(new_processed_text)

        #sort the tf-idf vectors by descending order of scores
        sorted_items = executeEmailTfIdf.sort_coo(X_tf1.tocoo())
    #    print(sorted_items)
        feature_names = executeEmailTfIdf.tf1_new.get_feature_names()

        #extract only the top n; n here is 10
        keywords = executeEmailTfIdf.extract_topn_from_vector(feature_names, sorted_items, 10)
    #    print(keywords)
        # now print the results
    #    print("\n===Keywords===")
    #    for k in keywords:
    #        print(orderId, k, keywords[k])
        keywordsList = list(keywords)
    #    print(keywords)
    #    print(orderId, keywordsList[0], keywordsList[1])
    #    print(keywordsList[0], keywordsList[1])
        return [orderId, keywordsList[0], keywordsList[1]]

    def execute():
        entries = os.scandir(os.getcwd() + '/data/testdata/')
        for i in entries:
            #print(i)
            executeEmailTfIdf.executeTFIDF(i.name)

    #def executeTFIDF(self, i):
    def executeTFIDF(self, mailcontent):
        processed_text = []
        #file = open(i[0], 'r', encoding="utf8", errors='ignore')
        #file = open(os.getcwd() + '/data/testdata/' + i, 'r', encoding="utf8", errors='ignore')
        #text = file.read().strip()
        #file.close()
        #print(text)
        allOrderId = re.findall(r'WS\d+|ws\d+|\d+\-\d+\-\d+', mailcontent)
        if len(allOrderId) > 0:
            orderId = allOrderId[0]
            #print(orderId)
            content_text = re.sub(r'WS\d+|ws\d+|\d+\-\d+\-\d+', "", mailcontent)
            content_text = str(executeEmailTfIdf.preprocess(content_text))
            #print(content_text)
            content_text = word_tokenize(content_text)
            #print(content_text)
            processed_text.append(content_text)
            #print(processed_text)
            tfidf_response = executeEmailTfIdf.apply_tfidf(orderId, processed_text)
            print(tfidf_response)
            return tfidf_response

#print(executeEmailTfIdf.execute())
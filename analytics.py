from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
import preprocessor as tweet_preprocessor
import re

class Analytics():

    def __init__(self,keywords):
        self.tb = Blobber(analyzer=NaiveBayesAnalyzer())
        self.keywords = keywords

    def preprocess(self,text):
        text = tweet_preprocessor.clean(text)
        word_list = re.findall("[\w]+",text)
        return word_list

    def sentiment(self,text):

        senti = self.tb(text)
        return {'polarity':senti.polarity,
                'subjectivity': senti.subjectivity}

    def relevant_keywords(self,word_list):

        relevant_keywords= []

        for key in keywords:
            if key in word_list:
                relevant_keywordsa.append(key)

        return {'relevant_keywords': relevant_keywords}

    def get_analytics(self,text):

        word_list = self.preprocess(text)
        cleaned_sentence = ' '.join(word_list)
        relevance_data = self.relevance(word_list)

        sentiment = self.sentiment(cleaned_sentence)
        relevant_keywords = relevance_data['relevant_keywords']

        return { 'sentiment': sentiment,
                 'relevant_keywords': relevant_keywords,
                 'is_relevant': True,
                 'text': text
                }

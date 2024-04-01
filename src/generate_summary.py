import json
import requests
from datetime import date, timedelta

class News:
    api_key = 'f50463cd13ed4a009e961148e1a90a05'
    url = 'https://newsapi.org/v2/everything'

    def __init__(self, list_of_keywords, word_limit, email_frequency, email):
        self.lst_keywords = list_of_keywords
        self.word_limit = word_limit
        self.email_freq = email_frequency
        self.email = email

    def _get_keyword_articles(self, lst_of_keywords, articles_from):
        #get 'from' query parameter
        todays_date = date.today()
        if articles_from is 'daily':
            oldest_article_from = str(todays_date - timedelta(days = 1))
        else:
            oldest_article_from = str(todays_date - timedelta(days = 7))
        for word in lst_of_keywords:
            params = {'apiKey': self.api_key, 'q': word, 'language': 'en', 'from': oldest_article_from}
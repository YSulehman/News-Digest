import json
import requests
from datetime import date, timedelta

class News:
    api_key = 'f50463cd13ed4a009e961148e1a90a05'
    url = 'https://newsapi.org/v2/everything'

    def __init__(self, list_of_keywords: list, word_limit: int, email_frequency: str, email: str):
        self.lst_keywords = list_of_keywords
        self.word_limit = word_limit
        self.email_freq = email_frequency
        self.email = email

        self._get_keyword_articles(self.lst_keywords, self.email_freq)

    def _get_keyword_articles(self, lst_of_keywords: list, articles_from: str):
        #get 'from' query parameter
        todays_date = date.today()
        if articles_from is 'daily':
            oldest_article_from = str(todays_date - timedelta(days = 1))
        else:
            oldest_article_from = str(todays_date - timedelta(days = 7))
        for word in lst_of_keywords:
            #specify query parameters
            params = {'apiKey': self.api_key, 'q': word, 'language': 'en', 'from': oldest_article_from, 'pageSize': 2}

            article_info = requests.get(self.url,params=params)
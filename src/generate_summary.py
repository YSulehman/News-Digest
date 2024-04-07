import json
import requests
from datetime import date, timedelta

class News:
    api_key = 'f50463cd13ed4a009e961148e1a90a05'
    url = 'https://newsapi.org/v2/everything' #search every article published by over 5,000 different sources in the last 5 years
    url_breaking = 'https://newsapi.org/v2/top-headlines' #provides live top and breaking headlines

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
            params = {'apiKey': self.api_key, 'q': word, 'language': 'en', 'from': oldest_article_from, 'pageSize': 1}

            article_request = requests.get(self.url,params=params)

            if article_request.status_code != 200:
                print(f'unsuccessful request, error code: {article_request.status_code} reason: {article_request.reason}')
            else:
                article_data = article_request.json()

                #get news article description
                articles = article_data['articles']
                for article in articles:
                    print(article['description'])

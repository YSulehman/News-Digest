import requests

class News:
    def __init__(self, list_of_keywords, word_limit, email_frequency, email):
        self.lst_keywords = list_of_keywords
        self.word_limit = word_limit
        self.email_freq = email_frequency
        self.email = email

    def _get_keyword_articles(self, lst_of_keywords):
        pass 
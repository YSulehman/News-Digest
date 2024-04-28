import os
import requests
from datetime import date, timedelta

#get api-key
news_api_key = os.environ.get('NEWS_API_KEY')
news_api_key = news_api_key.strip("'") #had issue with single quotes, it included these from the environment variable.

class News:
    headers = {'X-Api-Key': news_api_key}
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
        if articles_from == 'weekly':
            oldest_article_from = str(todays_date - timedelta(days = 7))
        for word in lst_of_keywords:
            #specify query parameters
            if articles_from == 'weekly':
                weekly_params = {'q': word, 'language': 'en', 'from': oldest_article_from, 'pageSize': 1, 'apiKey': news_api_key}
                #print(self.headers['X-Api-Key'])
                #print(weekly_params['apiKey'])
                article_request = requests.get(self.url,params=weekly_params, headers=self.headers)
                #article_request = requests.get(self.url,params=weekly_params)
            else:
                daily_params = {'q': word, 'country': 'gb','pageSize': 1}

                article_request = requests.get(self.url_breaking,params=daily_params, headers=self.headers)
            #print(article_request.url)

            if article_request.status_code != 200:
                print(f'unsuccessful request, error code: {article_request.status_code} reason: {article_request.reason}')
            else:
                article_data = article_request.json()

                #check if any results returned
                total_results = article_data['totalResults']
                if total_results == 0:
                    print('No relevant news articles found.')

                else:
                    #get news article description
                    articles = article_data['articles']
                    #print(len(articles))
                    for article in articles:
                        title = article['title']
                        article_content = article['description']
                        article_url = article['url']
                        #print(article_content)
                        print(title)
                        print(len(article_content))
                        print(article_url)
                        self._write_to_file(title, article_content, article_url, './test_article.txt')

    def _write_to_file(self, heading: str, contents: str, article_url: str, file_name: str):
        with open(file_name, 'w') as f:
            f.write(heading + '\n\n')
            f.write(contents + '\n\n')
            f.write(article_url)

if __name__=="__main__":
    n = News(['United'], 200, 'weekly', 'ysulehman@hotmail.com')

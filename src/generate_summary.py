import os
import smtplib
import requests
from openai import OpenAI
from email.message import EmailMessage
from datetime import date, timedelta

#get api-key, this was done specifically (?) for windows os. Is it necessary/applicable for linux? 
news_api_key = os.environ.get('NEWS_API_KEY')
news_api_key = news_api_key.strip("'") #had issue with single quotes, it included these from the environment variable.
openai_api_key = os.environ.get('OPENAI_API_KEY')

class News:
    headers = {'X-Api-Key': news_api_key}
    url = 'https://newsapi.org/v2/everything' #search every article published by over 5,000 different sources in the last 5 years
    url_breaking = 'https://newsapi.org/v2/top-headlines' #provides live top and breaking headlines

    def __init__(self, list_of_keywords: list, word_limit: int, email_frequency: str, recipient_email: str, sender_email: str):
        self.lst_keywords = list_of_keywords
        self.word_limit = word_limit
        self.email_freq = email_frequency
        self.recipient_email = recipient_email
        self.sender_email = sender_email

        #self._get_keyword_articles(self.lst_keywords, self.email_freq)

    def make_newsletter(self, lst_of_keywords: list, articles_from: str):
        #get 'from' query parameter
        todays_date = date.today()
        if articles_from == 'weekly':
            oldest_article_from = str(todays_date - timedelta(days = 7))
        for word in lst_of_keywords:
            #specify query parameters
            if articles_from == 'weekly':
                weekly_params = {'q': word, 'language': 'en', 'from': oldest_article_from, 'pageSize': 1, 'apiKey': news_api_key}
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
                        # get relevant information from news article
                        self.title = article['title']
                        self.article_content = article['description']
                        self.article_url = article['url']
                       
                        # optional write to file, more so for testing.
                        #self._write_to_file(title, article_content, article_url, './test_article.txt')
                        self.summary = self._gpt_summary(self.article_content)
                        
                        # after summarising, send email

    def _write_to_file(self, heading: str, contents: str, article_url: str, file_name: str):
        with open(file_name, 'w') as f:
            f.write(heading + '\n\n')
            f.write(contents + '\n\n')
            f.write(article_url)

    def _gpt_summary(self, text_to_summarise: str):
        """
        Summarise news article using OpenAI's GPT-3.5 model
        """
        client = OpenAI(api_key=openai_api_key)

        response = client.chat.completions.create(
            messages = [
                {'role': 'user',
                'content': text_to_summarise}],
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=25)

        summary = response['choices'][0]['message']['content']

        return summary 
    
    def send_email(recipient_email_address: str, sender_email_address: str, news_heading: str, news_contents: str, news_url: str):
        """
        Send email to recipient with news summary
        """
        msg = EmailMessage()
        msg.set_content(news_contents)
        msg['Subject'] = news_heading
        msg['From'] = sender_email_address
        msg['To'] = recipient_email_address

        # send email
        try:
            with smtplib.SMTP_SSL('smtp-mail.outlook.com', 587) as server:
                # make server connection secure
                server.starttls()
                server.login(sender_email_address, os.environ.get('EMAIL_PASSWORD'))
                server.send_message(msg)
        except Exception as e:
            print(f'Error sending email: {e}')


if __name__=="__main__":
    n = News(['United'], 200, 'weekly', 'ysulehman@hotmail.com')

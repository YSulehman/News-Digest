import argparse
from src.generate_summary import News

def list_of_keywords(arg):
    return arg.split(',')

def main(args):
    # parse arguments to pass to News class
    news_args = {
        'list_of_keywords': args.keywords,
        'word_limit': args.word_limit,
        'email_frequency': args.frequency,
        'email': args.email
    }

    news = News(**news_args)

    # make the newsletter content
    news.make_newsletter(args.keywords, args.frequency)

    # send the email
    news.send_email(args.email, news.title, news.summary, news.article_url)

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    #user defined functions as types for cl arguments!
    parser.add_argument('-kw', '--keywords', type=list_of_keywords, help='keywords for news search, comma separated')

    parser.add_argument('-frq', '--frequency', type=str, choices=['daily', 'weekly'], 
                        help='choose frequency of news summary')
    
    parser.add_argument('--email', type=str, help='email to send news story to')
    
    parser.add_argument('-wl', '--word_limit', type=int, default=300, help='a word limit on the news summary for each keyword')

    args = parser.parse_args()

    main(args)
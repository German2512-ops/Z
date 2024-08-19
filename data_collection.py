import tweepy
import requests
import praw
from config import news_api_key, reddit_config


def fetch_tweets(currency, date):
    auth = tweepy.OAuth1UserHandler(**twitter_config)
    api = tweepy.API(auth)
    query = f"{currency} since:{date} until:{date}"
    tweets = api.search(q=query, lang="en", count=100)
    return [tweet.text for tweet in tweets]

def fetch_news(currency, date):
    url = f'https://newsapi.org/v2/everything?q={currency}&from={date}&to={date}&sortBy=popularity&apiKey={news_api_key}'
    response = requests.get(url)
    articles = response.json().get('articles', [])
    return [article['title'] + " " + article['description'] for article in articles]

def fetch_reddit_posts(currency, date):
    reddit = praw.Reddit(**reddit_config)
    subreddit = reddit.subreddit('all')
    search_query = f"{currency} timestamp:{date}..{date}"
    posts = subreddit.search(search_query, syntax='cloudsearch')
    return [post.title + " " + post.selftext for post in posts]

def collect_data(currency, date):
    tweets = fetch_tweets(currency, date)
    news = fetch_news(currency, date)
    reddit_posts = fetch_reddit_posts(currency, date)
    return {'tweets': tweets, 'news': news, 'reddit': reddit_posts}



def collect_data(currency, date):
    tweets = fetch_tweets(currency, date)
    news = fetch_news(currency, date)
    reddit_posts = fetch_reddit_posts(currency, date)
    
    all_data = {
        'tweets': tweets,
        'news': news,
        'reddit': reddit_posts
    }
    
    return all_data


data = collect_data(currency, date)
print(data)
import praw
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="Bitcoin Predictor",
)

def scrape_subr(subr, limit=1500):
    subreddit = reddit.subreddit(subr)
    posts = []

    for post in subreddit.hot(limit=limit):
        posts.append({
            "time": post.created_utc,
            "title": post.title,
            "score": post.score,
            "num_comments": post.num_comments
        })

    return pd.DataFrame(posts)
    

def scrape():
    print("Scraping data from r/CryptoCurrency...")
    sub_crypto= scrape_subr("CryptoCurrency")
    print("Scraping data from r/Bitcoin...")
    sub_bitcoin = scrape_subr("Bitcoin")
    print("Scraping data from r/BitcoinMarkets...")
    sub_bitcoinmarkets = scrape_subr("BitcoinMarkets")
    print("Scraping data from r/btc...")
    sub_btc = scrape_subr("btc")
    print("Scraping data from r/CryptoMarkets...")
    sub_cryptomarkets = scrape_subr("CryptoMarkets")

    combined = pd.concat([sub_crypto, sub_bitcoin, sub_bitcoinmarkets, sub_btc, sub_cryptomarkets],
                          ignore_index=True)
    combined.to_csv("data/reddit_posts.csv", index=False)
    print("Saving data to data/reddit_posts.csv...")
    return
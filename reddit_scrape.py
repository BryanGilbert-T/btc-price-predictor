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

df = pd.read_csv("data/default.csv")
scraped = ["CryptoCurrency",
           "Bitcoin",
           "BitcoinMarkets",
           "btc",
           "CryptoMarkets"]


def scrape_subr(subr, limit=1500):
    subreddit = reddit.subreddit(subr)
    posts = []

    for post in subreddit.hot(limit=limit):
        posts.append({
            "time": post.created_utc,
            "title": post.title,
            "score": post.score,
            "num_comments": post.num_comments,
        })

    return pd.DataFrame(posts)
    

def scrape(subreddit_name):
    global df
    if subreddit_name in scraped:
        print("We already have that data")
        return
    
    print(f"Scraping data from r/{subreddit_name}...")
    sub_df = scrape_subr(subreddit_name)

    combined = pd.concat([df, sub_df], ignore_index=True)
    combined.to_csv("data/reddit_posts.csv", index=False)
    df = combined
    print("Saving data to data/reddit_posts.csv...")
    return
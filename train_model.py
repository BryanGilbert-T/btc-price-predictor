import pandas as pd

def prepare_data():
    reddit = pd.read_csv("data/reddit_posts.csv")
    btc = pd.read_csv("data/btc_prices.csv")

    reddit["datatime"] = pd.to_datetime(reddit["time"], unit='s')

    print(reddit)
    print()
    print(btc)



def train():
    prepare_data()

if __name__ == "__main__":
    train()

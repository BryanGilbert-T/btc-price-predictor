from reddit_scrape import scrape
from btc_price import fetch_btc_data

def main():
    fetch_btc_data()
    scrape()

    return


if __name__ == "__main__":
    main()
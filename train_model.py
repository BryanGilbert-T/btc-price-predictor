import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler


model = None
vectorizer = TfidfVectorizer(max_features=5)
scaler = StandardScaler()


def prepare_data():
    reddit = pd.read_csv("data/reddit_posts.csv")
    btc = pd.read_csv("data/btc_prices.csv")

    reddit["time"] = pd.to_datetime(reddit["time"], unit='s', utc=True)
    reddit["hour"] = reddit["time"].dt.floor("h")

    btc["hour"] = pd.to_datetime(btc["Datetime"]).dt.floor("h")
    btc["change"] = btc["Close"].diff().shift(-1)
    btc["label"] = (btc["change"] > 0).astype(int) # Up or Down

    merged = pd.merge(reddit, btc[["hour", "label"]], on="hour")

    global vectorizer, scaler
    X_title = vectorizer.fit_transform(merged["title"]).toarray()

    X_numeric = merged[["score", "num_comments"]].values

    X_numeric = scaler.fit_transform(X_numeric)

    X = np.hstack((X_title, X_numeric))

    y = merged["label"]

    return X, y


def inference(X, y, model_name):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    if(model_name == 'A'):
        model = XGBClassifier(eval_metric="logloss")
    elif(model_name == 'B'):
        model = RandomForestClassifier()
    elif(model_name == 'C'):
        model = LogisticRegression(max_iter=1000)
    else:
        print("We don't have the model yet")
        return
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Model Report:")
    print(classification_report(y_test, y_pred))
    return model


def test(title, upvote_num, comment_num):
    global vectorizer, scaler
    if model is None:
        print("Model is untrained, please train the model first")
        return
    
    vector = vectorizer.transform([title]).toarray()
    nums = scaler.transform(np.array([[float(upvote_num), float(comment_num)]]))
    X = np.hstack((vector, nums))
    y = model.predict(X)

    print(f"Based on our model, bitcoin will go {'up' if y == 1 else 'down'} in the next hour")

    return


def train(model_name):
    global model
    print("Preparing data...")
    X, y = prepare_data()
    print("Training A.I...")
    model = inference(X, y, model_name)
    return


if __name__ == "__main__":
    train('A')

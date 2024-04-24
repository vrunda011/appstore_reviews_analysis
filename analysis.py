# https://apps.apple.com/in/app/snapchat/id447188370?see-all=reviews
# https://apps.apple.com/in/app/instagram/id389801252
# https://apps.apple.com/in/app/sharechat-videos-status/id1440640105
# https://apps.apple.com/rus/app/ludo-king/id993090598

from app_store_scraper import AppStore
from pprint import pprint
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from numpy import exp
from tqdm import tqdm

model = AutoModelForSequenceClassification.from_pretrained("Kaludi/Reviews-Sentiment-Analysis", use_auth_token=True)
tokenizer = AutoTokenizer.from_pretrained("Kaludi/Reviews-Sentiment-Analysis", use_auth_token=True)

def classify_review(review_content):
    inputs = tokenizer(review_content, return_tensors="pt")

    outputs = model(**inputs)
    logits = outputs.logits[0].tolist()

    e = exp(logits)
    probs = e/e.sum()

    if probs[1]>probs[0]:
        return "Positive"
    else:
        return "Negative"

def analyse_appstore_reviews(url):
    url_parts = url.split("/")
    if url_parts[2] == "apps.apple.com" and url_parts[4] == "app":
        conntry = url_parts[3]
        app_name = url_parts[5]
    else:
        raise ValueError("Invalid URL.")
    
    app = AppStore(country=conntry, app_name=app_name)
    app.review(how_many=20)

    results = {"Positive":0,"Negative":0}
    for review in tqdm(app.reviews):
        review_content = review["review"]
        sentiment = classify_review(review_content=review_content)
        results[sentiment]+=1

    results["Positive"]=results["Positive"]/len(app.reviews)*100
    results["Negative"]=results["Negative"]/len(app.reviews)*100
    return results

if __name__=="__main__":
    url="https://apps.apple.com/in/app/instagram/id389801252"
    result = analyse_appstore_reviews(url=url)
    print(result)
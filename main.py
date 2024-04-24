"""Sentiment analysis of reviews posted on Appstore."""

from flask import Flask, render_template,request
from analysis import analyse_appstore_reviews

app = Flask(
    __name__, template_folder="frontend", static_folder="frontend", static_url_path=""
)

@app.route("/")
def home():
    return render_template("home_page/home.html")

@app.route("/analyse", methods =["POST"])
def analyse():
   url = request.form.get('url')
   result = analyse_appstore_reviews(url=url)
   return result

if __name__ == "__main__":
    app.run(debug=True)

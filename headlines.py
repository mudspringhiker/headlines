from flask import Flask, render_template
import feedparser

app = Flask(__name__)

RSS_FEEDS = {"nyt": "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
			 "cnn": "http://rss.cnn.com/rss/edition.rss",
			 "wsj": "http://www.wsj.com/xml/rss/3_7455.xml",
			 "sk": "http://feeds.feedburner.com/smittenkitchen",
			 "whole30": "http://www.whole30.com/feed"}

@app.route("/")
@app.route("/<publication>")
def get_news(publication="nyt"):
	feed = feedparser.parse(RSS_FEEDS[publication])
	return render_template("home.html", articles=feed['entries'])

if __name__ == '__main__':
	app.run(debug=True)

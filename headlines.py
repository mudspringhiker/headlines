from flask import Flask
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
	first_article = feed['entries'][0]
	return """<html>
	    <body>
	       <h1>Headlines</h1>
	       <b>{0}</b> <br/>
	       <i>{1}</i> <br/>
	       <p>{2}</p> <br/>
	    </body>
	 </html>""".format(first_article.get("title"), first_article.get("published"), \
	 			 first_article.get("summary"))

if __name__ == '__main__':
	app.run(debug=True)

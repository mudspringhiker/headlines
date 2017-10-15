import feedparser
from flask import Flask, render_template, request
import json
import urllib2
import urllib

app = Flask(__name__)

RSS_FEEDS = {"New York Times": "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
			 "CNN": "http://rss.cnn.com/rss/edition.rss",
			 "Wall Street Journal": "http://www.wsj.com/xml/rss/3_7455.xml",
			 "Inquirer": "http://www.inquirer.net/fullfeed",
			 "Rappler": "http://feeds.feedburner.com/rappler/"}

DEFAULTS = {'publication': 'Inquirer',
			'city': 'Los Banos, Philippines',
			'currency_from': 'USD',
			'currency_to': 'PHP'}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=5ce2cfacf40dc85add8e462b9c006165"

CURRENCY_URL = "https://openexchangerates.org/api/latest.json?app_id=5b63b748b6e84e81b2438b536f42ac53"

@app.route("/")
def home():
	# get customized headlines, based on user input or default
	publication = request.args.get('publication')
	if not publication:
		publication = DEFAULTS['publication']
	articles, publications = get_news(publication)
	# get customized weather based on user input or default
	city = request.args.get('city')
	if not city:
		city = DEFAULTS['city']
	weather = get_weather(city)
	# get customized currency based on user input or default
	currency_from = request.args.get("currency_from")
	if not currency_from:
		currency_from = DEFAULTS['currency_from']
	currency_to = request.args.get("currency_to")
	if not currency_to:
		currency_to = DEFAULTS['currency_to']
	rate, currencies = get_rate(currency_from, currency_to)
	return render_template("home.html", articles=articles, weather=weather,
		  					currency_from=currency_from, currency_to=currency_to,
		  					rate=rate, currencies=sorted(currencies),
		  					publications=RSS_FEEDS.keys(), publication=publication)


def get_news(query):
	if not query or query not in RSS_FEEDS:
		publication = DEFAULTS['publication']
	else:
		publication = query
	feed = feedparser.parse(RSS_FEEDS[publication])
	return feed['entries'], RSS_FEEDS.keys()


def get_weather(query):
	query = urllib.quote(query)
	url = WEATHER_URL.format(query)
	data = urllib2.urlopen(url).read()
	parsed = json.loads(data)
	weather = None
	if parsed.get("weather"):
		weather = {"description": parsed["weather"][0]["description"],
				   "temperature": parsed["main"]["temp"],
				   "city": parsed["name"],
				   "country": parsed['sys']['country']}
	return weather


def get_rate(frm, to):
	all_currency = urllib2.urlopen(CURRENCY_URL).read()
	parsed = json.loads(all_currency).get('rates')
	frm_rate = parsed.get(frm.upper())
	to_rate = parsed.get(to.upper())
	return (to_rate / frm_rate, parsed.keys())


if __name__ == '__main__':
	app.run(debug=True)



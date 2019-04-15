from flask import Flask, render_template, request, redirect, url_for
from flask_caching import Cache
import feedparser
import datetime

app = Flask(__name__,  static_folder="static")
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

def make_cache_key(*args, **kwargs):
    return request.url

# homepage
@app.route('/')
def index():
	feedlist = [{'name':'Awesome','url':'Awesome'},
				{'name':'Comic','url':'Comic'},
				{'name':'Dark Humor','url':'DarkHumor'},
				{'name':'Funny','url':'Funny'}]
	return render_template("index.html",feedlist=feedlist)

# RSS Feed Subpage, Cache content for 180 seconds for each subpage
@app.route('/rss/<name>')
@cache.cached(timeout=180, key_prefix=make_cache_key)
def rss(name):
	if name in ['Awesome','Comic','DarkHumor','Funny']:
		posts = get_posts(name)
		time = str(datetime.datetime.now()) + " " + str(request.url)

		return render_template("rss.html", name=name, posts=posts)
	else:
		return render_template("404.html"), 404

# Get RSS Feed content
def get_posts(name):
    posts = []
    url = 'https://9gag-rss.com/api/rss/get?code=9GAG' + name + '&format=1'
    posts.extend(feedparser.parse(url).entries)
    return posts


if __name__=="__main__":
	app.run()


import feedparser


def get_posts(name):
    posts = []
    url = 'https://9gag-rss.com/api/rss/get?code=9GAG' + name + '&format=1'
    posts.extend(feedparser.parse(url).entries)
    return posts


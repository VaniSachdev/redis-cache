from cachelib.redis import RedisCache
from flask import Flask, request, render_template, redirect, url_for
import redis 

app = Flask(__name__)
cache = RedisCache(host='localhost', port=6379)

@app.route('/')
def index():
  return redirect('/favorites')


@app.route('/favorites')
def favorites():
    favorite_items = cache.get('favorite_items')
    if favorite_items is None:
        favorite_items = []
    return render_template('favorites.html', favorite_items=favorite_items)

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    item = request.form.get('item')
    favorite_items = cache.get('favorite_items')
    if favorite_items is None:
        favorite_items = []

    if item not in favorite_items:
        favorite_items.append(item)
    cache.set('favorite_items', favorite_items, timeout=600)
    return redirect('/favorites')

@app.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    item = request.form.get('item')
    favorite_items = cache.get('favorite_items')
    try:
        favorite_items.remove(item)
    except:
        pass
    cache.set('favorite_items', favorite_items, timeout=600)
    return redirect('/favorites')

# http://clouddatafacts.com/heroku/heroku-flask-redis/flask_redis.html



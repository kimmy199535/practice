from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup


from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient(
    'mongodb://test:sparta@ac-xrfxwbs-shard-00-00.3oqrgfu.mongodb.net:27017,ac-xrfxwbs-shard-00-01.3oqrgfu.mongodb.net:27017,ac-xrfxwbs-shard-00-02.3oqrgfu.mongodb.net:27017/?ssl=true&replicaSet=atlas-8rq53x-shard-0&authSource=admin&retryWrites=true&w=majority',
    tlsCAFile = ca
)
db = client.sparta2

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'title': title,
        'image': image,
        'desc': desc,
        'star': star_receive,
        'comment': comment_receive
    }

    db.movie.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


@app.route("/movie", methods=["GET"])
def movie_get():
    movielist = list(db.movie.find({}, {'_id': False}))
    return jsonify({'movie': movielist})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

from flask import Flask, redirect, jsonify, request
from flask_redis import FlaskRedis
from datetime import datetime
from utils import redis_utils
import pymysql as sql
from configs import Config
from flask_sqlalchemy import SQLAlchemy
from Model import ShortCut

app = Flask(__name__)
app.config.from_object(Config)
redis_client = FlaskRedis(app)
db = SQLAlchemy(app)

@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/api/v1/urls", methods=['POST'])
def create_url():
    sec = 1800
    if request.method == 'POST':
        url = request.values['url']
        expireAt = request.values['expireAt']
        expire_time = datetime.strptime(
            expireAt, "%Y-%m-%dT%H:%M:%S%z")
        get_db = ShortCut.query.filter_by(url=url).first()
        if get_db.delete is True or get_db.expire_at < datetime.now():

            # redis 過期時間應改成短時間暫存
            sec = 1800
            set_url = redis_utils.create(url=url,sec=sec)

            get_db.delete= True
            get_db.expire_at= expire_time
            get_db.set_url = set_url

        else:
            set_url = get_db.set_url

        # 先從DB取得有沒有存過值？還是先看redis？
        set_url = redis_utils.create(url=url,sec=sec)
    return jsonify(
        id=set_url,
        shortUrl=f"http://{request.host}/"+set_url
    )

@app.route("/api/v1/urls/<path:url_id>", methods=['DELETE'])
def delete_url(url_id):
    get_db = ShortCut.query.filter_by(set_url=url_id).filter_by(delete=False).order_by(ShortCut.expire_at.desc()).first()
    get_db.delete = True
    return redis_utils.delete(url_id)

@app.route("/<path:url_id>", methods=['GET'])
def redirect_url(url_id):
    original_url = redis_utils.get(url_id)
    if original_url is None:
        get_db = ShortCut.query.filter_by(set_url=url_id).filter_by(delete=False).order_by(ShortCut.expire_at.desc()).first()
        if get_db.expire_at > datetime.now() or get_db is None:
            return jsonify(message="No Key Found")
        else:
            original_url = get_db.url
    return redirect(original_url.decode('utf-8'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)

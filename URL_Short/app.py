from flask import Flask, redirect, jsonify, request
from flask_redis import FlaskRedis
from datetime import datetime
from utils import mainfunction
from configs import Config
from flask_sqlalchemy import SQLAlchemy
from Model import ShortCut
from database import db

app = Flask(__name__)
app.config.from_object(Config)
redis_client = FlaskRedis(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/api/v1/urls", methods=['POST'])
def create_url():
    sec = 1800
    # 先取得 POST 資料
    if request.method == 'POST':
        data = request.json
        l_url = data.get('url')
        expireAt = data.get('expireAt')
        expire_time = datetime.strptime(
            expireAt, "%Y-%m-%dT%H:%M:%S%z")

        # 如果 Redis 有，回傳短網址
        s_url = redis_client.get(l_url)
        if s_url:
            s_url = s_url.decode('utf-8')
            get_db = ShortCut.query.filter_by(l_url=l_url).first()
            get_db.expire_at = expire_time
            get_db.delete = False
            db.session.commit()

            return jsonify(
                id=s_url,
                shortUrl=f"http://{request.host}/"+s_url
            )

        # 如果 Redis 沒有，MySQL 有。MySQL 回傳
        get_db = ShortCut.query.filter_by(l_url=l_url).first()

        if get_db:
            redis_client.set(get_db.s_url, l_url, ex=sec)
            redis_client.set(l_url, get_db.s_url, ex=sec)
            get_db.expire_at = expire_time
            get_db.delete = False
            db.session.commit()

            return jsonify(
                id=get_db.s_url,
                shortUrl=f"http://{request.host}/"+get_db.s_url
            )

        # 都沒有的情況下，往 DB 跟 Redis 建立這些資訊
        s_url = mainfunction.code(15)
        redis_client.set(s_url, l_url, ex=sec)
        redis_client.set(l_url, s_url, ex=sec)
        new_shortcut = ShortCut(l_url=l_url, s_url=s_url,
                                expire_at=expire_time, delete=False)
        db.session.add(new_shortcut)
        db.session.commit()

    return jsonify(
        id=s_url,
        shortUrl=f"http://{request.host}/"+s_url
    )


@app.route("/api/v1/urls/<path:s_url>", methods=['DELETE'])
def delete_url(s_url):
    get_db = ShortCut.query.filter_by(s_url=s_url).filter_by(
        delete=False).order_by(ShortCut.expire_at.desc()).first()
    if not get_db:
        return "URL not found"

    get_db.delete = True
    db.session.commit()
    l_url = redis_client.get(s_url)
    redis_client.delete(s_url)
    redis_client.delete(l_url)
    return 'Success'


@app.route("/<path:s_url>", methods=['GET'])
def redirect_url(s_url):
    l_url = redis_client.get(s_url)
    if l_url:
        l_url = l_url.decode('utf-8')
        return redirect(l_url)

    get_db = ShortCut.query.filter_by(s_url=s_url).filter_by(
        delete=False).order_by(ShortCut.expire_at.desc()).first()
    if get_db:
        if get_db.expire_at > datetime.now():
            return redirect(get_db.l_url)
    return jsonify(
        message='No ShortUrl Found'
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

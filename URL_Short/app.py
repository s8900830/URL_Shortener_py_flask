from flask import Flask, redirect, jsonify, request
from utils import mainfunction
from flask_redis import FlaskRedis
import datetime
import pymysql as sql
from configs import Config

app = Flask(__name__)
app.config.from_object(Config)
redis_client = FlaskRedis(app)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/api/v1/urls", methods=['POST'])
def create_url():
    if request.method == 'POST':
        url = request.values['url']
        expire_at = request.values['expireAt']
        set_url = mainfunction.code(15)
        expire_time = datetime.datetime.strptime(
            expire_at, "%Y-%m-%dT%H:%M:%S%z")
        remain_time = (
            expire_time - datetime.datetime.now(expire_time.tzinfo))
        redis_client.set(set_url, url,  ex=remain_time)
    return jsonify(
        id=set_url,
        shortUrl=f"http://{request.host}/"+set_url
    )


@app.route("/api/v1/urls/<path:url_id>", methods=['DELETE'])
def delete_url(url_id):
    redis_client.delete(url_id)
    return 'Success'


@app.route("/<path:url_id>", methods=['GET'])
def redirect_url(url_id):
    original_url = redis_client.get(url_id)
    if original_url is None:
        return jsonify(message="No Key Found")
    else:
        return redirect(original_url.decode('utf-8'))
    # return redirect(str(redirect_url))

# @app.route("/goto/<path:url>", methods=['GET'])
# def _goto(url):
#     return redirect(url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)

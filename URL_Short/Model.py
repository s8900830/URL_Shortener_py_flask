from flask import Flask
from datetime import datetime
from configs import Config
from database import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


class ShortCut(db.Model):
    __tablename__ = 'ShortCut'
    id = db.Column('id', db.Integer, primary_key=True)
    s_url = db.Column('set', db.String(100))
    l_url = db.Column('url', db.String(100))
    expire_at = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    delete = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, s_url, l_url, expire_at, delete):
        self.s_url = s_url
        self.l_url = l_url
        self.expire_at = expire_at
        self.delete = delete


if __name__ == "__main__":
    app.run(debug=True, port=5100)

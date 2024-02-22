from flask import Flask
from datetime import datetime
from configs import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class ShortCut(db.Model):
    __tablename__ = 'ShortCut'
    id = db.Column('id', db.Integer, primary_key=True)
    set_url = db.Column('set', db.String(100))
    url = db.Column('url',db.String(100))
    expire_at = db.Colume(db.DateTime, nullable=False,
        default=datetime.utcnow)
    delete = db.Column(db.Boolean,default=False, nullable=False)

    def __init__(self, set_url, url,expire_at,delete):
        self.set_url = set_url
        self.url = url
        self.expire_at = expire_at
        self.delete = delete

if __name__ =="__main__":
    db.create_all()
    app.run(debug=True)
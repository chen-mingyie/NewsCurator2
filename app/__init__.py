from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nxgcqxkheabnvl:a32d538696f1722181abaf886e8fd4d48814585209a4696ac52542a181be2ff6@ec2-3-223-9-166.compute-1.amazonaws.com:5432/df3tpvo9k97eiu'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model/UserPreferences.sqlite3'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/news_curator'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b1b4046de436f6:1a31a7d6@us-cdbr-east-02.cleardb.com/heroku_3098ea224707aaa'
app.newsapp_active_user = ""
db = SQLAlchemy(app)


from app import routes

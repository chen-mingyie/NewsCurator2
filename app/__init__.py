from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/news_curator'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b1b4046de436f6:1a31a7d6@us-cdbr-east-02.cleardb.com/heroku_3098ea224707aaa'
app.newsapp_active_user = ""
db = SQLAlchemy(app)


from app import routes

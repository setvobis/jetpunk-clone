from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '540494ddd19dd0b296b347b0cbd3ffc6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jet.db'
db = SQLAlchemy(app)
bcr = Bcrypt(app)
login_m = LoginManager(app)
login_m.login_view = 'login'
login_m.login_message_category = 'warning'

from jetskunk import routes
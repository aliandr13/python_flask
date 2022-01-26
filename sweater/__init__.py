from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'some secret and very long key 123#'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234pass@localhost/py_sweater'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

from sweater import models, routes

db.create_all()

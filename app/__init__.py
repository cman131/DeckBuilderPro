from flask import Flask
from app import dbconnect
#from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

from app import views#, models

from flask import Flask,url_for,request,render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite.///databse.sqlite3'
db=SQLAlchemy(app)


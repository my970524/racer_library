from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from db_connect import db
from models import *
from views import api

app = Flask(__name__)
app.secret_key = 'affsfsfsdf'
app.register_blueprint(api.bp)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/racer_library"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)


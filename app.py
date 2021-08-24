from flask import Flask
from db_connect import db
import config
from models import *

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(config)

    app.secret_key = config.SECRET_KEY

    from views import api
    app.register_blueprint(api.bp)

    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI

    db.init_app(app)

    with app.app_context():
        db.create_all()    

    return app



if __name__ == "__main__":
    create_app().run(debug=True)


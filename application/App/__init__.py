from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from App.models import User
from dotenv import load_dotenv

def create_app(env="PRODUCTION"):
    load_dotenv(override=True)
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    if env == "PRODUCTION":
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    elif env == "TESTING":
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI_TEST")
        app.config["TESTING"] = True
 
    with app.app_context():
        from App.models import db
        db.init_app(app)
        migrate = Migrate(app, db, render_as_batch=True)
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login'

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        from App.views.auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from App.views.predict import pred as predict_blueprint
        app.register_blueprint(predict_blueprint)

    return app
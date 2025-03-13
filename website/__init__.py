from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from os import path
import os

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'i like bri with all my heart'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: Disable track modifications

    db.init_app(app)
    migrate.init_app(app, db)  # Initialize migrations

    from .models import User, Note  # Import models after initializing db

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    create_database(app)  # Ensure this runs properly

    return app

def create_database(app):
    if not path.exists(f'{DB_NAME}'):  # Directly use DB_NAME for SQLite db
        with app.app_context():
            db.create_all()
            print('Created Database!')
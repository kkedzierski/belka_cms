from flask import Flask
from belka.config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'main.sign_in'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    migrate = Migrate(app, db)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from belka.admin_panel.routes import main_panel
    from belka.authentication_panel.routes import authentication
    from belka.main_website.routes import website

    app.register_blueprint(main_panel)
    app.register_blueprint(authentication)
    app.register_blueprint(website)

    return app

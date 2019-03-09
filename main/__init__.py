from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from main.config import Config

# app.config.update(dict(
#     SECRET_KEY="powerful secretkey",
#     WTF_CSRF_SECRET_KEY="a csrf secret key"
# ))

db = SQLAlchemy()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from main.users.routes import users
    from main.primary.routes import primary
    from main.messages.routes import messages
    app.register_blueprint(users)
    app.register_blueprint(primary)
    app.register_blueprint(messages)

    return app




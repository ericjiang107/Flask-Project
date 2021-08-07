from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .models import db, User
from flask_migrate import Migrate
from .models import login_manager
from .api.routes import api
from .models import ma
from .helpers import JSONEncoder
from flask_cors import CORS

base = Flask(__name__)
base.config.from_object(Config)
db.init_app(base)
login_manager.init_app(base)
ma.init_app(base)

migrate = Migrate(base, db)

base.register_blueprint(site)
base.register_blueprint(auth)
base.register_blueprint(api)

login_manager.login_view = 'auth.signin' # Redirecting back to signin

base.json_encoder = JSONEncoder

CORS(base)
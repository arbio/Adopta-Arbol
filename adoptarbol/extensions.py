# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf.csrf import CSRFProtect
from flask_flatpages import FlatPages
from flask_hookserver import Hooks
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
admin = Admin(name='Admin Adopta Árbol', base_template='admin/adoptarbol.html')
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
pages = FlatPages()
api_manager = APIManager(flask_sqlalchemy_db=db)
hooks = Hooks(url='/hooks')
cors = CORS

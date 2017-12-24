# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template, jsonify

from adoptarbol import public, user, tree
from adoptarbol.assets import assets
from adoptarbol.extensions import bcrypt, cache, csrf_protect, db, debug_toolbar, \
    login_manager, migrate, pages, api_manager, hooks
from adoptarbol.settings import ProdConfig

import subprocess
import requests


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    try:
        register_hooks(app)
    except Exception:
        pass

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        if app.debug:
            return requests.get('http://localhost:8080/{}'.format(path)).text
        return render_template("index.html")

    return app


def register_extensions(app):
    """Register Flask extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    pages.init_app(app)
    api_manager.init_app(app)
    hooks.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(tree.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_hooks(app):
    def ping(data, delivery):
        return 'pong'
    hooks.register_hook('ping', ping)

    def new_code(data, delivery):
        print('New push to %s' % data['ref'])
        try:
            cmd_output = subprocess.check_output(
                ['git', 'pull', 'origin', 'master'],)
            return jsonify({'msg': str(cmd_output)})
        except subprocess.CalledProcessError as error:
            print("Code deployment failed", error.output)
            return jsonify({'msg': str(error.output)})
        return 'Thanks'
    hooks.register_hook('push', new_code)

    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None

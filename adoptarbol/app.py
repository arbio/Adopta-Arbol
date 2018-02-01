# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import os
import subprocess

from flask import Flask, jsonify, render_template

from adoptarbol import public, tree, user
from adoptarbol.extensions import (admin, api_manager, bcrypt, cache, cors, db, debug_toolbar, hooks,  # csrf_protect
                                   login_manager, migrate, pages)
from adoptarbol.settings import DevConfig, ProdConfig


def create_dev_app():
    return create_app(config_object=DevConfig)


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__, static_url_path=None, static_folder='../frontend/dist/static')
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    try:
        register_hooks(app)
    except Exception:
        pass

    return app


def register_extensions(app):
    """Register Flask extensions."""
    admin.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    # csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    pages.init_app(app)
    api_manager.init_app(app)
    hooks.init_app(app)
    cors(app, resources={r'/api/*': {'origins': '*'}})
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
            os.chdir('frontend')
            cmd_output = cmd_output + subprocess.check_output(
                ['npm', 'run', 'build'],)
            os.chdir('..')
            return jsonify({'msg': str(cmd_output)})
        except subprocess.CalledProcessError as error:
            print('Code deployment failed', error.output)
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

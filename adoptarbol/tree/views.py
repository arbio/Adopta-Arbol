
"""Tree API, including trees and sponsorships."""
from flask import Blueprint, jsonify, redirect, url_for

from adoptarbol.extensions import api_manager
from adoptarbol.tree.models import Sponsorship, Tree

# from flask_login import login_required, login_user, logout_user

# from adoptarbol.user.models import User

blueprint = Blueprint('tree', __name__, static_folder='../flask_static')

api_manager.create_api(Tree)
api_manager.create_api(Sponsorship)


@blueprint.route('/api')
def api_docs():
    """convenience api docs access."""
    return redirect(url_for('public.page', path='api'))


@blueprint.route('/random/tree')
@blueprint.route('/api/trees/_random')
def random_tree_endpoint():
    """random tree."""
    return jsonify(dict(Tree.random()))

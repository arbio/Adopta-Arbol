
"""Tree API, including trees and sponsorships."""
from flask import Blueprint, jsonify, redirect, url_for

from adoptarbol.database import RestrictedModelView
from adoptarbol.extensions import admin, api_manager, db
from adoptarbol.tree.models import Sponsorship, Tree

# from flask_login import login_required, login_user, logout_user


blueprint = Blueprint('tree_manager', __name__, static_folder='../static')

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


admin.add_view(RestrictedModelView(Tree, db.session))
admin.add_view(RestrictedModelView(Sponsorship, db.session))

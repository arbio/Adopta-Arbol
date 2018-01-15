
"""Tree API, including trees and sponsorships."""
import json
from flask import Blueprint, jsonify, redirect, url_for, request

from adoptarbol.database import RestrictedModelView
from adoptarbol.extensions import admin, db
from adoptarbol.tree.models import Sponsorship, Tree

# from flask_login import login_required, login_user, logout_user


blueprint = Blueprint('tree_manager', __name__, static_folder='../static')


@blueprint.route('/api')
def api_docs():
    """convenience api docs access."""
    return redirect(url_for('public.page', path='api'))


@blueprint.route('/random/tree')
@blueprint.route('/api/trees/_random')
def random_tree_endpoint():
    """random tree."""
    return jsonify(dict(Tree.random()))


@blueprint.route('/api/trees/adopt', methods=['POST', 'GET'])
def adopt_tree_endpoint():
    """random tree."""
    data = request.get_json(force=True)['params']
    print(data)

    s = Sponsorship()
    s.reference = json.dumps(data)
    s.amount = data['amount']
    s.currency = 'USD'
    s.status = 'alpha-test'
    s.save()

    return jsonify(data)


admin.add_view(RestrictedModelView(Tree, db.session))
admin.add_view(RestrictedModelView(Sponsorship, db.session))

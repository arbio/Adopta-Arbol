
"""Tree API, including trees and sponsorships."""
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_required, login_user, logout_user

from adoptarbol.user.models import User
from adoptarbol.tree.models import Tree, Sponsorship
from adoptarbol.extensions import api_manager 

from random import randint

blueprint = Blueprint('tree', __name__, static_folder='../static')

api_manager.create_api(Tree)
api_manager.create_api(Sponsorship)

@blueprint.route('/random/tree')
def random_tree():
    """tree list."""
    random_id = randint(1, Tree.query.count())
    tree = Tree.query.offset(random_id).first()
    # tree = Tree.query.filter(Tree.code == code).first_or_404()
    return jsonify(tree)

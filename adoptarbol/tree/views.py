
"""Tree API, including trees and sponsorships."""
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_required, login_user, logout_user

from adoptarbol.user.models import User
from adoptarbol.tree.models import Tree, Sponsorship
from adoptarbol.extensions import api_manager 

blueprint = Blueprint('tree', __name__, static_folder='../static')

api_manager.create_api(Tree)
api_manager.create_api(Sponsorship)

@blueprint.route('/API/tree/<code>')
def tree(code):
    """tree list."""
    tree = Tree.query.filter(Tree.code == code).first_or_404()
    return jsonify(tree)

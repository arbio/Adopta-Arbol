
"""Tree API, including trees and sponsorships."""
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_required, login_user, logout_user

from adoptarbol.user.models import User
from adoptarbol.tree.models import Tree, Sponsorship

blueprint = Blueprint('tree', __name__, static_folder='../static')

@blueprint.route('/API/tree/<code>')
def tree(code):
    """tree list."""
    tree = Tree.query.filter(Tree.code == code).first_or_404()
    return jsonify(tree)

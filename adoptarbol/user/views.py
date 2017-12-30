# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required

from adoptarbol.database import RestrictedModelView
from adoptarbol.extensions import admin, db
from adoptarbol.user.models import User

blueprint = Blueprint('user_manager', __name__, url_prefix='/users', static_folder='../static')


@blueprint.route('/')
@login_required
def members():
    """List members."""
    return render_template('users/members.html')


admin.add_view(RestrictedModelView(User, db.session))

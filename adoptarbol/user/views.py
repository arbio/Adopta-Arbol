# -*- coding: utf-8 -*-
"""User views."""
import os

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from adoptarbol.database import RestrictedModelView
from adoptarbol.extensions import admin, db
from adoptarbol.user.models import User
from loader import load

blueprint = Blueprint('user_manager', __name__, url_prefix='/users', static_folder='../static')


@login_required
@blueprint.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            full_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(full_filename)
            load(full_filename)
            return redirect(url_for('user_manager.upload_file',
                                    filename=filename))
    return render_template('users/members.html')


admin.add_view(RestrictedModelView(User, db.session))

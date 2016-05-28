# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_required, login_user, logout_user

from adoptarbol.extensions import login_manager, pages
from adoptarbol.public.forms import LoginForm
from adoptarbol.user.forms import RegisterForm
from adoptarbol.user.models import User
from adoptarbol.tree.models import Tree, Sponsorship
from adoptarbol.utils import flash_errors

from random import choice

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/page/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    template = page.meta.get('template', 'public/flatpages.html')
    return render_template(template, page=page)

@blueprint.route('/api/pages/<path:path>/_random')
def get_random_item(path):
    page = pages.get_or_404(path)
    lines =  [line for line in page.body.split('\n') if line.startswith('- ')]
    return choice(lines)[2:]

@blueprint.route('/api/pages/<path:path>')
def get_page(path):
    page = pages.get_or_404(path)
    result = page.meta
    result['body'] = page.body
    result['html'] = page.html
    result['path'] = page.path
    return jsonify(page.meta)


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/selected/<int:tree_id>')
def home(tree_id=None):
    """Home page."""
    if not tree_id:
        tree = Tree.random()
    else:
        tree = Tree.get_by_id(tree_id)

    before_it = tree.before.id
    after_it = tree.after.id

    total = Tree.query.count()
    banner_a = get_random_item('frases')
    banner_b = get_random_item('sabiasque')

    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('public/home.html', form=form, tree=tree, total=total, \
                            image=tree.image, banner_a=banner_a, banner_b=banner_b, \
                            before_it=before_it, after_it=after_it)


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        User.create(username=form.username.data, email=form.email.data, password=form.password.data, active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)

# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from random import choice, randint

from flask import current_app as app
import requests
from flask import Blueprint, flash, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask import Response, stream_with_context
from flask_login import login_required, login_user, logout_user

from adoptarbol.extensions import login_manager, pages
from adoptarbol.public.forms import LoginForm, SponsorshipForm
from adoptarbol.tree.models import Tree
from adoptarbol.user.forms import RegisterForm
from adoptarbol.user.models import User
from adoptarbol.utils import flash_errors, secure_path

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/page/<path:path>/')
def page(path):
    path = secure_path(path.lower())
    page = pages.get_or_404(path)
    template = page.meta.get('template', 'public/flatpages.html')
    return render_template(template, page=page)


@blueprint.route('/api/pages/<path:path>/_random')
def get_random_item(path):
    path = secure_path(path.lower())
    page = pages.get_or_404(path)
    lines = [line for line in page.body.split('\n') if line.startswith('- ')]
    return choice(lines)[2:]


@blueprint.route('/api/pages/<path:path>')
def get_page(path):
    page = pages.get_or_404(path)
    result = page.meta
    result['body'] = page.body
    result['html'] = page.html
    result['path'] = page.path
    return jsonify(page.meta)


@blueprint.route('/home')
def home(tree_id=None):
    """Home page."""
    if not tree_id:
        tree = Tree.random()
    else:
        tree = Tree.get_by_id(tree_id)

    nav = image = None
    if tree:
        try:
            if not tree.comments:
                tree.comments = get_random_item('sobremi')
        except AttributeError:
            tree.comments = get_random_item('sobremi')

        nav = {}
        nav['before'] = tree.before.id
        nav['after'] = tree.after.id

        image = tree.image
    else:
        tree = Tree(code=0)

    count = {}
    count['total'] = Tree.query.count()
    count['sponsored'] = Tree.adopted()
    # clever way to get next multiple of 5
    count['target'] = count['sponsored'] + (5 - count['sponsored'] % 5)
    if count['target'] > count['total']:
        count['target'] = count['total']

    banner = {}
    banner['a'] = get_random_item('frases')
    banner['c'] = get_random_item('sabiasque')
    banner['d'] = get_random_item('porqueadoptar')

    return render_template('public/home.html', tree=tree, count=count,
                           image=image, banner=banner, nav=nav)


@blueprint.route('/home/adopt/')
@blueprint.route('/home/adopt/<int:tree_id>')
def adopt(tree_id=None):
    """adopt a tree."""
    if not tree_id:
        tree = Tree.random()
        if not tree:
            return redirect(url_for('public.page', path='error/notree'))
        return redirect(url_for('public.adopt', tree_id=tree.id))
    else:
        tree = Tree.get_by_id(tree_id)

    terminos = pages.get('terminosadopcion')

    print(request.args.get('sandbox'))
    form = SponsorshipForm(request.form, sandbox=request.args.get('sandbox'))

    """
    explanation = {'wood': u'Es maderable',
                   'bird': u'Es hogar de aves',
                   'mammal': u'Es hogar de mamíferos',
                   'soil': u'Es mejorador del suelo',
                   'community': u'Es importante para las comunidades nativas',
                   'medicine': u'Es medicinal'}
    """

    try:
        tree.comments = tree['comments']
    except AttributeError:
        tree.comments = get_random_item('sobremi')

    """
    functions = []  # tree ecosystemic icons
    for function in tree.function.split(','):
        functions.append({'icon': '%s.png' % function,
                          'desc': explanation[function]})
    """

    return render_template('public/adopt.html', tree=tree, terminos=terminos,
                           image=tree.image, form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user_manager.upload_file')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('public/login.html', loginform=form)


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
    form = RegisterForm(request.form, csrf=False)
    if form.validate_on_submit():
        User.create(username=form.username.data, email=form.email.data, password=form.password.data, active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/debug/')
def debug():
    raise Exception


@blueprint.route('/', defaults={'path': ''})
@blueprint.route('/<path:path>')
def catch_all(path):
    # path = secure_path(path)  # XXX - check

    print('***** ', path)
    if app.debug:
        url = 'http://localhost:3000/{}'.format(path)
        req = requests.get(url, stream=True)
        return Response(stream_with_context(req.raw.stream(decode_content=False)),
                        content_type=req.headers['content-type'])
        # return requests.get('http://localhost:8080/{}'.format(path)).text

    return send_from_directory('../frontend/dist/', 'index.html')


# Custom static data
@blueprint.route('/_nuxt/<path:filename>')
def front_assets(filename):
    # filename = secure_path(filename)  # XXX - check
    if app.debug:
        return catch_all('_nuxt/' + filename)
    return send_from_directory('../frontend/dist/_nuxt', filename)


@blueprint.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

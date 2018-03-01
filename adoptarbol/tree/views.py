# -*- coding: utf-8 -*-

"""Tree API, including trees and sponsorships."""
import datetime
import json
import os
import subprocess

from flask import Blueprint, jsonify, redirect, request, url_for, render_template
from flask import current_app as app
from flask_mail import Message

from adoptarbol.database import RestrictedModelView
from adoptarbol.extensions import admin, db, mail
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
    s.period = data['years']
    s.currency = 'USD'
    s.status = 'beta-test'
    s.save()

    if len(data['trees']) == 1:
        subject = '¡Gracias por adoptar un árbol!'
    elif len(data['trees']) > 1:
        subject = '¡Gracias por adoptar ' + str(len(data['trees'])) + ' árboles!'

    msg = Message(subject,
                  sender='equipo@somosazucar.org',
                  recipients=[data['email']],
                  bcc=['equipo@somosazucar.org'])

    body = """¡Hola!\n\n¡Gracias por proteger el bosque! Por favor encuentra
    adjunto a este correo tu(s) certificado(s) de adopción.\n\n
    Términos y Condiciones de la Adopción: Gracias a la generosa donación recibida,
el árbol adoptado recibirá atención Lorem ipsum dolor sit amet consectetur
adipiscing, elit velit rutrum leo. Odio curabitur senectus magna lacinia neque
tempus pulvinar, ullamcorper facilisi diam condimentum molestie bibendum ad,
massa penatibus laoreet ultrices dapibus habitant. Faucibus etiam scelerisque
felis ullamcorper nunc imperdiet lacus, dapibus ultricies sollicitudin habitant
sapien aliquam sagittis, viverra ante penatibus eu porttitor aenean.
"""

    iso_date = str(datetime.datetime.now())[:10]
    for tree_id in data['trees']:
        tree = db.session.query(Tree).filter(Tree.id == tree_id).first()
        print('saving tree svg cert for ' + tree.common_name)

        svg = render_template('cert/certificado_plantilla_light.svg',
                              common_name=tree.common_name,
                              scientific_name=tree.scientific_name,
                              family=tree.family,
                              coord_utm_e=tree.coord_utm_e,
                              coord_utm_n=tree.coord_utm_n,
                              sponsored_on=iso_date,
                              sponsor=data['sponsor'] or 'Anónimo')
        output_filename = 'certs/' + iso_date + '_sponsored_' + str(tree_id) + '.svg'
        with open(output_filename, 'w') as text_file:
            text_file.write(svg)

        pdf_filename = output_filename[:-3] + 'pdf'
        subprocess.call(['inkscape', output_filename, '-z', '-A', pdf_filename])
        with app.open_resource('../' + pdf_filename) as fp:
            msg.attach(os.path.basename(pdf_filename), 'application/pdf', fp.read())

    msg.body = body
    mail.send(msg)

    return jsonify(data)


admin.add_view(RestrictedModelView(Tree, db.session))
admin.add_view(RestrictedModelView(Sponsorship, db.session))

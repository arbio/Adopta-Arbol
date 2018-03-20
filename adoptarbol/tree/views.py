# -*- coding: utf-8 -*-

"""Tree API, including trees and sponsorships."""
import json
import os
import subprocess
from datetime import datetime

from flask import Blueprint, jsonify, redirect, request, url_for, render_template
from flask import current_app as app
from flask_mail import Message

from adoptarbol.database import RestrictedModelView
from adoptarbol.extensions import admin, db, mail, csrf
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


@blueprint.route('/api/trees/_pending')
def pending_tree_endpoint():
    if request.args.get('page'):
        return redirect(url_for('treesapi0.treesapi', page=request.args.get('page')))
    num_per_page = request.args.get('results_per_page', 9)
    pending_tree = db.session.query(Tree).filter(Tree.sponsored_until == None).first()  # noqa
    page = int(int(pending_tree.id) / int(num_per_page)) + 1
    return redirect(url_for('treesapi0.treesapi', page=page))


@csrf.exempt
@blueprint.route('/api/trees/adopt', methods=['POST', 'GET'])
def adopt_tree_endpoint():
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
                  recipients=[data['email']],
                  bcc=['equipo@somosazucar.org'])

    body = """¡Hola!\n\n¡Gracias por proteger el bosque!\n
    Por favor encuentra adjunto a este correo tu(s) certificado(s) de adopción.\n

    Términos y Condiciones de la Adopción
    -------------------------------------

    Gracias a la generosa donación recibida el árbol adoptado
    recibirá atención Lorem ipsum dolor sit amet consectetur
    adipiscing, elit velit rutrum leo. Odio curabitur senectus
    magna lacinia neque tempus pulvinar, ullamcorper facilisi
    diam condimentum molestie bibendum ad, massa penatibus
    laoreet ultrices dapibus habitant. Faucibus etiam
    scelerisque felis ullamcorper nunc imperdiet lacus, dapibus
    ultricies sollicitudin habitant sapien aliquam sagittis,
    viverra ante penatibus eu porttitor aenean. """

    if '@' in data['giftTo']:
        body = body + '\n\nSe envió la siguiente comunicación:\n\n'
        body = body + '¡Se ha protegido el bosque! Alguien ha adoptado uno o varios ' + \
            'árboles amazónicos y te lo han dedicado a ti.\n\nDe: ' + data['giftFrom'] + \
            '\n\nPara: ' + data['giftTo'] + '\n\nDedicatoria:\n  ' + data['giftDedication']
        if '@' in data['giftTo']:
            body = body + '\n\n Un email será enviado a ' + data['giftTo']
        else:
            body = body + '\n\n Para notificar al beneficiario se debe usar una dirección de correo.'

    today = datetime.utcnow()
    iso_date = str(today)[:10]
    if today.month == 2 and today.day == 29:
        today.day = 28
    sponsored_until = today.replace(today.year + data['years'])
    iso_until = str(sponsored_until)[:10]
    data['svg_certs'] = []
    data['pdf_certs'] = []
    for tree_id in data['trees']:
        tree = db.session.query(Tree).filter(Tree.id == tree_id).first()
        tree.sponsored_until = sponsored_until
        tree.sponsorship = s.id
        tree.save()

        # Make the certificate
        print('saving tree svg cert for ' + tree.common_name)

        sponsor = data['giftTo'] if data['giftTo'] else\
            data['sponsor'] if data['sponsor'] else\
            'Anonimo'

        svg = render_template('cert/certificado_plantilla_light.svg',
                              common_name=tree.common_name,
                              scientific_name=tree.scientific_name,
                              family=tree.family,
                              coord_utm_e=tree.coord_utm_e,
                              coord_utm_n=tree.coord_utm_n,
                              sponsored_on=iso_date,
                              sponsored_until=iso_until,
                              sponsor=sponsor)
        output_filename = 'certs/Cert_Adopt_' + iso_date + '_ID' + str(tree_id) + '.svg'
        data['svg_certs'].append(output_filename)
        with open(output_filename, 'w') as text_file:
            text_file.write(svg)

        pdf_filename = output_filename[:-3] + 'pdf'
        subprocess.call(['inkscape', output_filename, '-z', '-A', pdf_filename])
        data['pdf_certs'].append(pdf_filename)
        with app.open_resource('../' + pdf_filename) as fp:
            msg.attach(os.path.basename(pdf_filename), 'application/pdf', fp.read())

    msg.body = body
    try:
        mail.send(msg)
    except ConnectionRefusedError:
        print('Error: Connection refused sending mail.')


    if '@' in data['giftTo']:
        msg.recipients = [data['giftTo']]
        msg.body = '¡Se ha protegido el bosque! Alguien ha adoptado uno o varios ' + \
                   'árboles amazónicos y te lo han dedicado a ti.\n\nDe: ' + data['giftFrom'] + \
                   '\n\nPara: ' + data['giftTo'] + '\n\nDedicatoria:\n  ' + data['giftDedication']
        mail.send(msg)

    return jsonify(data)


admin.add_view(RestrictedModelView(Tree, db.session))
admin.add_view(RestrictedModelView(Sponsorship, db.session))

import os

from flask.ext.script import Manager

from adoptarbol.app import create_app
from adoptarbol.database import db
from adoptarbol.settings import DevConfig, ProdConfig

from adoptarbol.tree.models import Tree

CONFIG = ProdConfig if os.environ.get('adoptarbol_ENV') == 'prod' else DevConfig

app = create_app(CONFIG)
manager = Manager(app)

import csv

with app.app_context():
    with open("dataloader/Inventario.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            tree = {
                "code":row[1].decode('UTF-8'),
                "common_name":row[2].decode('UTF-8'),
                "scientific_name":row[3].decode('UTF-8'),
                "family":row[4].decode('UTF-8'),
                "coord_utm_e":float(row[5]),
                "coord_utm_n":float(row[6]),
                "diameter":int(row[7]),
                "height":int(row[8]),
                "comments":row[9].decode('UTF-8')
                }
            Tree.create (**tree)

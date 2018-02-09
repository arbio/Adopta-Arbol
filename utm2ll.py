import os
import utm
import tqdm
from adoptarbol.app import create_app
from adoptarbol.tree.models import Tree
from adoptarbol.settings import DevConfig, ProdConfig

CONFIG = ProdConfig if os.environ.get('adoptarbol_ENV') == 'prod' else DevConfig


def coonvert():
    for tree in tqdm.tqdm(Tree.query(), total=Tree.query().count()):
        utm_e = tree.coord_utm_e
        utm_n = tree.coord_utm_n
        lat, lon = utm.to_latlon(utm_e, utm_n, 19, northern=False)
        tree.coord_lat = lat
        tree.coord_lon = lon
        tree.save()


if __name__ == '__main__':
    app = create_app(CONFIG)

    with app.app_context():
        coonvert()

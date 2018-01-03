import csv

from dateutil.parser import parse

from adoptarbol.tree.models import Tree


def load(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        header = next(reader)

        def pos_for(field):
            return header.index(field)

        def float_or_none(string):
            try:
                return(float(string))
            except ValueError:
                return None

        for row in reader:
            # codigo = str(row[pos_for('codigo')]),
            print('Procesando ', row)

            tree = {'code': row[pos_for('codigo')],
                    'common_name': row[pos_for('especie')],
                    'scientific_name': row[pos_for('cientifico')],
                    'family': row[pos_for('familia')],
                    'coord_utm_e': float_or_none(row[pos_for('utm_x')].replace(',', '.')),
                    'coord_utm_n': float_or_none(row[pos_for('utm_y')].replace(',', '.')),
                    'coord_utm_zone_letter': row[pos_for('utm_zone')],
                    'coord_utm_zone_n': row[pos_for('utm_south')],
                    'coord_lat': float_or_none(row[pos_for('lat')].replace(',', '.')),
                    'coord_lon': float_or_none(row[pos_for('long')].replace(',', '.')),
                    'photo': row[pos_for('fotos')],
                    'diameter': row[pos_for('dia')],
                    'height': row[pos_for('alt')],
                    'circ': row[pos_for('circ')],
                    'base_area': float_or_none(row[pos_for('areabasal')].replace(',', '.')),
                    'size_class': row[pos_for('clasetamano')],
                    'quality': float_or_none(row[pos_for('calidad')].replace(',', '.')),
                    'relevance': row[pos_for('relevancia')],
                    'notes': row[pos_for('notas')],
                    'phenology': row[pos_for('fenologia')],
                    'observation': row[pos_for('obs')],
                    'surveyed_on': parse(row[pos_for('fechahora')]),
                    }

            t = Tree(**tree)
            t.save()


"""
if __name__ == '__main__':
    app = create_app(CONFIG)
    manager = Manager(app)

    with app.app_context():
        load()
"""

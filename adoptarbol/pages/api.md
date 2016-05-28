title: Documentación del API

# Documentación del API

Documentación general del motor de API REST: [flask-restless](http://flask-restless.readthedocs.io/en/stable/requestformat.html)

## Ejemplos

### Árboles

- **Lista:** [/api/trees](/api/trees)

- **Un registro:** [/api/trees/1](/api/trees/1)

        {
          "code": "404-1",
          "comments": "",
          "common_name": "Ubos",
          "coord_lat": -12.172729420173384,
          "coord_lon": -69.3876664399811,
          "coord_utm_e": 457825.75,
          "coord_utm_n": 8654316.08,
          "coord_utm_zone_letter": "L",
          "coord_utm_zone_n": 19,
          "diameter": 95,
          "family": "",
          "height": 20,
          "id": 1,
          "photo": "",
          "scientific_name": "Spondias mombin",
          "sponsor": []
        }

- **Imágenes:** [/api/trees/1/image](/api/trees/1/image)
    
    El campo `exists` es falso si **no** se encontró imagen específica del individuo o en su defecto la especie.

        {
            "exists": false,
            "src": "static/images/reference_tree.jpg"
        }

- **Paginación:** [/api/trees?page=2](/api/trees?page=2)

- **Al azar:** [/api/trees/\_random](/api/trees/_random)

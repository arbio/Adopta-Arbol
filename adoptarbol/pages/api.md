title: Documentación del API

# Documentación del API con ejemplos

Documentación general del motor de API REST: [flask-restless](http://flask-restless.readthedocs.io/en/stable/requestformat.html)

## Árboles

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

- **Después/Antes:**
    - [/api/trees/2/after](/api/trees/2/after) devuelve el anterior (relativo al índice, en este caso, 2)
    - [/api/trees/2/before](/api/trees/2/before) devuelve el posterior<br><br>

- **Al azar:** [/api/trees/\_random](/api/trees/_random)

## Páginas

Las páginas corresponden en el sistema de archivo con el directorio  `pages` y son archivos en formato [*Markdown*](http://daringfireball.net/projects/markdown/).

El api permite obtener un ítem de lista al azar (para colocar una frase sola).

- **Ítem al azar:** [/api/pages/*&lt;pagina&gt;*/\_random](/api/pages/frases/_random) (ej. `pagina` : frases)

- **Una página:** [/api/pages/sabiasque](/api/pages/sabiasque)

Las páginas disponibles pueden ser consultadas (y editadas) en el directorio [`pages/`](https://github.com/icarito/arbio-azucar-adoptarbol/tree/master/adoptarbol/pages).

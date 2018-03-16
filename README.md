Adopta Arbol
============

Plataforma de Adopción de Árboles

Aplicación Web cliente - servidor

Adopta Árbol puede leer archivos CSV con información geográfica, ubicarlos en un mapa y ofrecerlos para adopción.
La adopción genera un certificado en formato PDF que será enviado por e-mail a los auspiciadores y cuidantes de árboles.

Adopta Árbol es Software Libre y se distribuye bajo los términos de la licencia AGPLv3.

Los archivos CSV corresponden con aquellos creados por el sistema [Censa Árbol](https://github.com/arbio/Censa-Arbol).

Una iniciativa de Arbio y SomosAzucar.

Desarrollo
==========

Adopta - Árbol consiste en dos aplicaciones. Un back-end en [Flask](http://flask.pocoo.org/) (`adoptarbol/`) y un frontend en [Nuxt.js](https://nuxtjs.org/) (`frontend/`).

Durante el desarrollo es necesario ejecutar ambas:
```
$ gunicorn adoptarbol.app:create_dev_app\(\) --threads=4 -b 0.0.0.0:5000 --graceful-timeout 4 --reload
```
y, aparte:
```
nuxt --spa frontend/
```

Es necesario haber instalado los requerimientos y bibliotecas de ambas: `pip install -r requirements.txt` y `npm install` respectivamente.

También se necesita usar el servidor web *"Gunicorn"* con **hilos** para poder sincronizar con el frontend durante el desarrollo.

Instalación en Producción
=========================

En este caso se desactiva la depuración y se utiliza la configuración de producción (base de datos, etc).
```
adoptarbol/ $ gunicorn adoptarbol.app:create_app\(\) --threads=4 -b 0.0.0.0:5000 --graceful-timeout 4 --reload
```

En este caso ya no es necesario ejecutar la aplicación frontend, pero sí generarla para publicar la última versión:
```
frontend/ $ nuxt build --spa
```

La configuración tanto de desarrollo como producción se encuentra en `adoptarbol/settings.py`.

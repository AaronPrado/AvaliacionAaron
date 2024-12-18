# Integración de scripts en Python con CityBikes

## 🚴‍♂️ Descripción

Proyecto que recibe información en tiempo real de estaciones de bicicletas públicas en A Coruña. Permite el guardado de estos datos en CSV y Parquet para el análisis de datos. Almacenamiento de datos en MongoDB

## ⚙️ Guía de Inicio
Clonado del repositorio:

    git clone git@github.com:AaronPrado/AvaliacionAaron.git

Execución del Docker Compose

    docker compose up -d

Dentro de la carpeta "scripts" se encuentran los scripts de almacenaje de datos en "scripts/Almacenar" que obtiene los datos
de la api y los añade periodicamente a la base de datos Mongo.

En la carpeta "scripts/Leer" se encuentra el script que transforma la información de la base de datos en un .CSV y un .parquet

Finalmente, en "scripts/Extra" se encuentran unas versiones modificadas de los anteriores scripts utilizando un API diferente, en este caso, obtenemos la localización de la Estación Espacial Internacional

## 📓 Dependecias utilizadas

 - `requests`
 - `time`
- `pymongo`
- `pandas`
- `datetime`

## 🌐 APIs y DockerHub

Para el proyecto base utilizamos el endpoint **http://api.citybik.es/v2/networks/bicicorunha**
Mientras que para el extra utilicé un API que muestra la localización de la Estación Espacial Internacional **http://api.open-notify.org/iss-now.json**

La imagen utilizada para el script de almacenamiento se encuentra en:
```bash
docker pull aaronprado/almacenar-almacenar_datos
```

## 🤖 Automatización del contenedor de Docker

Añade en "Repository Secrets" de Github tu Token personal generado en Docker Hub

Añade el token en DOCKER_USERNAME

DOCKERHUB_TOKEN
```bash
name: ci

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      -
        name: Checkout
        uses: actions/checkout@v4
      -
        name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      -
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      -
        name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
```

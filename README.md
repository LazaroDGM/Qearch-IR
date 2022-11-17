# Qearch-IR
Sistema de Recuperación de Información de Documentos Local

## Requisitos
Le recomendamos crear un entorno virtual para ejecutar el proyecto. Trabajamos con la version `3.9` de `python`. Es necesario instalar los módulos `nltk`, `ir_datasets`, `regex` y el framework `django`. Puede ejecutar los siguientes comandos en consola para instalar estos.
```
pip install nltk
pip install regex
pip install --upgrade ir_datasets
pip install Django==4.1.3
```
## Conjunto de datos procesados
Los modelos implementados trabajarán principalmente con unos datos preprocesados. La dirección de estos datos se debe especificar dentro del archivo `\boolean\boolean_model.py` en la variable `DIR`:
```
...
# TODO Modificar la dirección de los datos de ocurrencia extraídos
DIR = '/data'
...
```

## Ejecución del servidor
Para iniciar el servidor basta con ejecutar el comando en consola:
```
python manage.py run server
```

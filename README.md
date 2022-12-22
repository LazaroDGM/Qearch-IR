# Qearch-IR
Sistema de Recuperación de Información de Documentos Local

## Requisitos
Le recomendamos crear un entorno virtual para ejecutar el proyecto. Trabajamos con la version `3.9` de `python`. Es necesario instalar los módulos `nltk`, `ir_datasets`, `regex` y el framework `django`. Puede ejecutar los siguientes comandos en consola para instalar estos.
```
pip install nltk
pip install regex
pip install --upgrade ir_datasets
pip install Django==4.1.3
pip install fire
```
o puede utilizar el archivo `requirements.txt` para instalar todos los requisitos en su entorno virtual. Tenga que en el caso de `nltk` puede ser necesario que se necesite descargar el lematizador de WordNet y la colección de stopwords.
## Conjunto de datos procesados
Los modelos implementados trabajarán principalmente con unos datos preprocesados. La dirección de estos datos se debe especificar dentro del archivo `/sriApp/modelos/boolean_model.py`, `/sriApp/modelos/vectorial.py`, y `/sriApp/modelos/lsi_model.py` (de cada modelo) en la variable `DIR`:
```
...
# TODO Modificar la dirección de los datos de ocurrencia extraídos
DIR = 'sriApp/procesed_data/'
...
```
Por defecto esa es la dirección de donde se leerán los datos procesados.
## Procesar datos
Dentro del archivo `/extract/extract_lg.py` se encuentran las funciones con las cuales se pueden extraer los datos necesarios para los modelos. Además hay creado varios script que puede cargar para al menos generar las colecciones que por defecto se usan:
```
python3 extract/script_frec.py 'cranfield' 'sriApp/procesed_data/cranfield/frec.json'
python3 extract/script_SVD.py 'sriApp/procesed_data/cranfield/' 1400 200
python3 extract/script_idf.py 'sriApp/procesed_data/cranfield/frec.json' 'sriApp/procesed_data/cranfield/idf.pkl' 1400
python3 extract/script_terms.py 'sriApp/procesed_data/cranfield/frec.json' 'sriApp/procesed_data/cranfield/terms.pkl'

python3 extract/script_frec.py 'beir/cqadupstack/gaming' 'sriApp/procesed_data/beir/cqadupstack/gaming/frec.json'
python3 extract/script_idf.py 'sriApp/procesed_data/beir/cqadupstack/gaming/frec.json' 'sriApp/procesed_data/beir/cqadupstack/gaming/idf.pkl' 45301
python3 extract/script_terms.py 'sriApp/procesed_data/beir/cqadupstack/gaming/frec.json' 'sriApp/procesed_data/beir/cqadupstack/gaming/terms.pkl'

python3 extract/script_frec.py 'beir/cqadupstack/physics' 'sriApp/procesed_data/beir/cqadupstack/physics/frec.json'
python3 extract/script_idf.py 'sriApp/procesed_data/beir/cqadupstack/physics/frec.json' 'sriApp/procesed_data/beir/cqadupstack/physics/idf.pkl' 38316
python3 extract/script_terms.py 'sriApp/procesed_data/beir/cqadupstack/physics/frec.json' 'sriApp/procesed_data/beir/cqadupstack/physics/terms.pkl'

python3 extract/script_frec.py 'beir/cqadupstack/mathematica' 'sriApp/procesed_data/beir/cqadupstack/mathematica/frec.json'
python3 extract/script_idf.py 'sriApp/procesed_data/beir/cqadupstack/mathematica/frec.json' 'sriApp/procesed_data/beir/cqadupstack/mathematica/idf.pkl' 16705
python3 extract/script_terms.py 'sriApp/procesed_data/beir/cqadupstack/mathematica/frec.json' 'sriApp/procesed_data/beir/cqadupstack/mathematica/terms.pkl'
```
## Ejecución del servidor
Para iniciar el servidor basta con ejecutar el comando en consola:
```
python manage.py run server
```

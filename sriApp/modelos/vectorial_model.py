import json
from .parser_vectorial import ParserVectorial
from .SortedValueDataSet import SortedValueDataSet, ValueData

datasets = {
    "beir/arguana": {'count': 8674},
    #"beir/dbpedia-entity": {'count': 4635922},
    "beir/fiqa": {'count': 57638},
    "beir/cqadupstack/android": {'count': 22998},
    "beir/cqadupstack/english": {'count': 40221},
    "beir/cqadupstack/gaming": {'count': 45301},
    "beir/cqadupstack/gis": {'count': 37637},
    "beir/cqadupstack/mathematica": {'count': 16705},
    "beir/cqadupstack/physics": {'count': 38316},
    "beir/cqadupstack/programmers": {'count': 32176},
    "beir/cqadupstack/stats": {'count': 42269},
    "beir/cqadupstack/tex": {'count': 68184},
    "beir/cqadupstack/unix": {'count': 47382},
    "beir/cqadupstack/webmasters": {'count': 17405},
    "beir/cqadupstack/wordpress": {'count': 48605},
    "cranfield": {'count': 1400}
}

# TODO Modificar la dirección de los datos de ocurrencia extraídos
DIR = 'sriApp/procesed_data/'

def open_frec(name_file):
    try:
        with open(name_file, 'rb') as file:
            # Cargar su contenido y crear un diccionario
            datos = json.load(file)
            for key, value in datos.items():
                s = SortedValueDataSet()
                for doc, frec in value.items():                    
                    s.add(ValueData(int(doc), frec))
                datos[key] = s
            return datos
    except:
        return None

class VectorialModel():
    def __init__(self, name_dataset) -> None:        
        self.name_dataset = name_dataset
        datos = open_frec(DIR + name_dataset + '/frec.json')
        
        self.parser = ParserVectorial(terms=datos, universe=set(range(0, datasets[name_dataset]['count'])))
        print('CARGADO Modelo Vectorial')

    def SearchResuts(self, exp: str):
        results = self.parser.eval(exp)        
        return results

    def SearchIndex(self, exp: str, umbral= 0.5):
        results = self.parser.eval(exp)        
        return [datavalue.data for datavalue in results if datavalue.value > umbral]

    def ModDataset(self, name_dataset):
        datos = open_frec(DIR + name_dataset + '/frec.json')
        del(self.parser)
        self.parser = ParserVectorial(terms=datos, universe=set(range(0, datasets[name_dataset]['count'])))
        self.name_dataset = name_dataset

    def DestroyDataset(self):
        self.parser.DestroyDataset()
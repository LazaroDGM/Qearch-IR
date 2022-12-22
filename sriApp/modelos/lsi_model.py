import json
from .SortedValueDataSet import SortedValueDataSet, ValueData
import numpy as np
import pickle
from .parser_lsi import ParserLSI

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

def open_Dk_Rq(name_file):    
    try:
        Dk = np.load(name_file + 'Dk.npy')
        Rq = np.load(name_file + 'Rq.npy')
        with open(name_file+'terms.pkl', 'rb') as tf:
            terms = pickle.load(tf)
        return Dk, Rq, terms
    except:
        return None

class LSIModel():
    def __init__(self, name_dataset) -> None:        
        self.name_dataset = name_dataset
        Dk, Rq, terms = open_Dk_Rq(DIR + name_dataset + '/')
        self.parser = ParserLSI(terms=terms, Dk=Dk, Rq=Rq, universe=set(range(0, datasets[name_dataset]['count'])))
        print('CARGADO Modelo Latente')

    def SearchResuts(self, exp: str):
        results = self.parser.eval(exp)        
        return results

    def SearchIndex(self, exp: str, umbral= 0.):
        results = self.parser.eval(exp)        
        return [datavalue.data for datavalue in results if datavalue.value > umbral][:40]

    def ModDataset(self, name_dataset):        
        del(self.parser)
        Dk, Rq, terms = open_Dk_Rq(DIR + name_dataset + '/')
        self.parser = ParserLSI(terms=terms, Dk=Dk, Rq=Rq, universe=set(range(0, datasets[name_dataset]['count'])))
        self.name_dataset = name_dataset

    def DestroyDataset(self):
        del(self.parser)

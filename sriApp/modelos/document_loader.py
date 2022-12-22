from ir_datasets import load
import numpy as np
import pickle

metadata = {
    'cranfield' : {
        'title': 1,
        'text': 2
    },
    'beir/cqadupstack/gaming': {
        'title': 2,
        'text': 1
    },
    'beir/cqadupstack/physics': {
        'title': 2,
        'text': 1
    },
    'beir/cqadupstack/mathematica': {
        'title': 2,
        'text': 1
    },
}


class DocumentLoader():

    def __init__(self) -> None:
        self._name_dataset = None
    
    def ModDataset(self, name_dataset, dir):
        '''
        Actualiza el dataset por defecto
        '''
        self._name_dataset = name_dataset
        with open(dir + name_dataset + '/idf.pkl', 'rb')as ft:
            self._idf = pickle.load(ft)
        

    def SearchDescriptionDocsByIndex(self, indexs):
        '''
        Carga de la base de datos por defecto la descripcion de los documentos
        correspondientes a los indices `indexs`
        '''
        l = []
        dataset = load(self._name_dataset)
        index_title = metadata[self._name_dataset]['title']
        for i in indexs:
            #print(i)
            title = dataset.docs_iter()[i:i+1][0][index_title]
            l.append((title,))
        return l

    def SearchDocByIndex(self, index):
        dataset = load(self._name_dataset)
        index_title = metadata[self._name_dataset]['title']
        index_text = metadata[self._name_dataset]['text']
        doc = dataset.docs_iter()[index:index+1][0]
        return (doc[index_title], doc[index_text])

    def get_term_idf(self):
        return dict(self._idf)




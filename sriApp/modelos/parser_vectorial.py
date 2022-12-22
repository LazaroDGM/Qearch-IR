from nltk import WordNetLemmatizer
import regex as re
from .SortedValueDataSet import preproc_frec, ValueData, SortedValueDataSet
import bisect
import numpy as np


# Definición del lenguaje de consultas
# Asociativo a la derecha
# E -> TX
# X -> &E | |E | epsilon
# T -> t | (E) | ~T

# Clase para parsear expresiones booleanas y evaluarlas
class ParserVectorial:
    def __init__(self, terms: dict, universe= set(), lemmatizer = WordNetLemmatizer()) -> None:
        if len(universe) == 0:
            for set in terms.values():
                universe = universe.union(set)
        # Diccionario de términos con conjunto de documentos en los que se encuentra
        self.terms = terms
        # Conjunto de todos los documentos (solo índices)
        self.universe = universe
        # Para normalizar las palabras
        self.lemmatizer = lemmatizer

    # Evaluador de la expresión booleana
    def eval(self, exp: str):
        tokens = {}
        preproc_frec(exp, tokens, -1)
        tf_q = np.array([sortedSet.get_DataByIndex(0).data for sortedSet in tokens.values()])
        tf_q = tf_q / np.max(tf_q)

        idf = np.zeros(len(tf_q))
        for i, token in enumerate(tokens.keys()):
            ni = len(self.terms.get(token, []))
            if ni != 0:
                idf[i] = np.log(len(self.universe)/ ni)
            else:
                idf[i] = 0
        
        alpha= 0.4
        w_q = (alpha + (1 - alpha) * tf_q) * idf

        set_union = set()
        for key in tokens.keys():
            if key in self.terms:
                set_union = set_union.union(self.terms[key].to_set())
        
        w_d = np.zeros(len(tokens))
        sorted = []
        for index_doc in set_union:
            for i, token in enumerate(tokens.keys()):
                if token in self.terms:
                    w_d[i] = self.terms[token].get_DataByValue(index_doc, 0)
                else:
                    w_d[i] = 0
            w_d = w_d / np.max(w_d)
            bisect.insort_left(sorted, ValueData(self.sim(w_d, w_q), index_doc))  

        sorted.reverse()
        return sorted

    def sim(self, w_d, w_q):
        return w_d.dot(w_q) / (np.linalg.norm(w_d, 2) * np.linalg.norm(w_q, 2))
            

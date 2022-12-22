from nltk import WordNetLemmatizer, FreqDist
import regex as re
from .SortedValueDataSet import preproc_frec, ValueData, SortedValueDataSet, normalize
import bisect
import numpy as np
from numpy.linalg import norm

# Definición del lenguaje de consultas
# Asociativo a la derecha
# E -> TX
# X -> &E | |E | epsilon
# T -> t | (E) | ~T

# Clase para parsear expresiones booleanas y evaluarlas
class ParserLSI:
    def __init__(self, terms: dict , Dk, Rq, universe= set()) -> None:
        if len(universe) == 0:
            for set in terms.values():
                universe = universe.union(set)
        # Diccionario de términos con conjunto de documentos en los que se encuentra
        self.terms = terms
        # Conjunto de todos los documentos (solo índices)
        self.universe = universe
        # Para normalizar las palabras
        self.Dk = Dk
        self.Rq = Rq

    # Evaluador de la expresión booleana
    def eval(self, exp: str):        
        items  = FreqDist(normalize(exp)).items()
        q = np.zeros(len(self.terms))
        for term, frec in items:
            if term in self.terms:
                q[self.terms[term]] = 1

        qk = self.Rq.dot(q)        
        
        sortedSet = SortedValueDataSet()
        for j, dj in enumerate(self.Dk):
            if len(dj[dj>0]) > 0:
                sim_dj = self.sim(qk, dj)
                sortedSet.add(ValueData(sim_dj, j))
        sorted = reversed(sortedSet.to_numpy())
        return sorted

    def sim(self, w_d, w_q):
        norms = ((np.linalg.norm(w_d, 2) * np.linalg.norm(w_q, 2)))
        if norms > 0:
            return w_d.dot(w_q) / norms
        else:
            return 0
            

import os
from os.path import exists, join
from math import log10, sqrt
from time import time
# from colorama import Fore, init
# from fileinput import input

# init()
class VectorialModel:
    d_titles: [str] = []
    d_descriptions: [str] = []
    d_t_frequency_table: [dict[int, int]] = []                  # lista donde el indice se asocia al indice de los documentos, 
    d_t_weight_table: [dict[int, float]] = []                   # Matriz de pesos de los terminos en cada documento
    d_max_frequency: [int] = []                                 # Frecuencia maxima de un termino por cada documento
    t_indexes : dict[str, int] = {}                             # Indice correspondiente a cada termino
    t_ocurence_in_docs: [int] = []                              # Cuanto ocurre cada termino en los documentos

    tf = lambda self, d, t: self.d_t_frequency_table[d][t] / self.d_max_frequency[d]
    idf = lambda self, t: log10(len(self.d_t_frequency_table) / self.t_ocurence_in_docs[t])

    def __init__(self, path):
        self.ReadDocsFrom(path)

    def ReadDocsFrom(self, path):
        print(f'Reading \"{path}\"path')
        start = time()
        if not exists(path): raise FileNotFoundError(f"No existe el directorio {path}")
        Docs_directory : [str] = os.listdir(path)
        count: int = 0
        for d, doc_dir in enumerate(Docs_directory):
            self.d_t_frequency_table.insert(d, {})
            self.d_max_frequency.insert(d, 1)
            # print(f'reading \"{doc_dir}\" file ')
            self.d_titles.insert(d, doc_dir)
            with open(join(path, doc_dir)) as file:
                for l, line in enumerate(file):
                    if l == 0: self.d_descriptions.insert(d, line)
                # for line in input(join(path, doc_dir)):
                    for word in line.split(" "):
                        if word in self.t_indexes: 
                            word_index: int = self.t_indexes[word]
                            if word_index not in self.d_t_frequency_table[d]:
                                self.d_t_frequency_table[d][word_index] = 1
                                self.t_ocurence_in_docs[word_index]+= 1
                            else: self.d_t_frequency_table[d][word_index]+= 1

                            if self.d_t_frequency_table[d][word_index] > self.d_max_frequency[d]: 
                                self.d_max_frequency[d]+= 1
                        else:
                            word_index = self.t_indexes[word] = len(self.t_indexes)
                            self.t_ocurence_in_docs.insert(word_index, 1)
                            self.d_t_frequency_table[d][word_index] = 1
        end = time()
        print(f'Finish Reading. It took {end - start} seconds')
        self.UpdateWeigths()

    def UpdateWeigths(self):
        for d in range(len(self.d_t_frequency_table)):
            self.d_t_weight_table.insert(d, {})
            for t, t_frequency in self.d_t_frequency_table[d].items():
                self.d_t_weight_table[d][t] =  self.tf(d, t) * self.idf(t)
                # if d == 1: 
                    # print(f'{Fore.GREEN}{t}{Fore.WHITE}: {Fore.YELLOW}{self.d_t_weight_table[d][t]}{Fore.WHITE}')
        
    def sim(self, d, q_w_vector, q_norm):
        d_w_vector: dict[int, float] = self.d_t_weight_table[d]
        scalar_product: int = 0
        d_norm: int = 0
        for t, w_d_t in d_w_vector.items():
            if t in q_w_vector:
                scalar_product += w_d_t * q_w_vector[t]
            d_norm += w_d_t**2
        # print(f'd_norm: {d_norm}, \n q_norm: {q_norm}')
        denominador = sqrt(d_norm) * q_norm
        return (scalar_product / denominador) if denominador != 0 else 0.

    def getSim(self, q_array, q_alpha = 0):
        q_t_frequencies: dict[str, int] = {}
        q_max_frequency: int = 1
        
        for term in q_array:
            if term not in self.t_indexes: continue                                                  # term esta tanto en la consulta como en el corpus
            if term not in q_t_frequencies: q_t_frequencies[term] = 1
            else: 
                q_t_frequencies[term] += 1
                if q_t_frequencies[term] > q_max_frequency: q_max_frequency+= 1

        # print(f'q_t_frequencies: {Fore.YELLOW}{q_t_frequencies}{Fore.WHITE}')
        q_norm: int = 0
        _q_w_array: dict[int, float] = {}
        # print(f'q_t_frequencies: {q_t_frequencies}')

        for term, t_frequency in q_t_frequencies.items():
            t_index = self.t_indexes[term]
            # print(f'term: {term}, idf(term): {self.idf(t_index)}')
            w_q_t = (q_alpha + (1-q_alpha) * (t_frequency / q_max_frequency)) * self.idf(t_index)
            # print(f'term: {Fore.YELLOW}{term}{Fore.WHITE}, w_q_t: {Fore.YELLOW}{w_q_t}{Fore.WHITE}')
            q_norm += w_q_t**2
            _q_w_array[t_index] = w_q_t
        # print(f'q_norm: {q_norm}')
        
        return lambda d_index: self.sim(d_index, _q_w_array, sqrt(q_norm))

    def SortDocumentsRankingBy(self, q_array, q_alpha = 0):
        # print("entre al metodo de ordenacion del rangking")
        # print(f"y self.d_t_frequency_table tiene length= {len(self.d_t_frequency_table)}")
        sim_func = self.getSim(q_array, q_alpha)
        docs_ranking:[int] = []
        docs_ratings:[int] = []
        for d in range(len(self.d_t_frequency_table)):
            # print(f'sim_func({d}): {Fore.YELLOW}{sim_func(d)}{Fore.WHITE}')
            docs_ratings.append(sim_func(d))
            docs_ranking.append(d)
            for i in range(d, 0, -1):
                if docs_ratings[i] <= docs_ratings[i - 1]: break
                #region swap [i-1]  <-> [i]
                rank = docs_ranking[i];
                rate = docs_ratings[i];

                docs_ranking[i] = docs_ranking[i-1];
                docs_ratings[i] = docs_ratings[i-1];

                docs_ranking[i-1] = rank;
                docs_ratings[i-1] = rate;

                #endregion
        return docs_ranking





# vectorial = VectorialModel("Docs")

# for d, doc_vector in enumerate(vectorial.d_t_weight_table):
#     if d != 1: continue
#     print(f'{Fore.RED} document {d} {Fore.WHITE}')
#     for term, t in vectorial.t_indexes.items():
#         if t not in doc_vector: continue
#         print(f'term{Fore.GREEN} \"{term}\" {Fore.WHITE}: {doc_vector[t]}')
    
# print(vectorial.idf(vectorial.t_indexes["made"]))
# print(vectorial.SortDocumentsRankingBy(["different", "angles"]))
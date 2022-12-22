import json
import numpy as np
import pickle
from SortedValueDataSet import normalize
from ir_datasets import load
import nltk



def extract_frec(name_dataset, destint_path):
    '''
    Extrae un diccionario de terminos que indexan diccionarios de documentos-frecuencia.
    Ademas se serializa con `pickle` y se guarda en un directorio.

    `name_dataset`: Nombre del dataset

    `destint_path`: Nombre del directorio donde se guardara el diccionario serializado con `pickle`
    '''
    terms = {}
    index = 0
    for doc in load(name_dataset).docs_iter():
        tokens = normalize(doc.text)
        for token, frec in nltk.FreqDist(tokens).items():
            dict_doc = terms.get(token, dict())
            dict_doc[index] = dict_doc.get(index,0) + frec
            terms[token] = dict_doc
        index+=1
        if index % 5000 == 0:
            print(index // 5000)
    with open(destint_path, 'w') as tf:
        json.dump(terms, tf)

def extract_tf_idf(name_dataset, destint_path, count_documents):
    '''
    Extrae un diccionario de terminos que indexan diccionarios de documentos-frecuencia.
    Ademas se serializa con `pickle` y se guarda en un directorio.

    `name_dataset`: Nombre del dataset

    `destint_path`: Nombre del directorio donde se guardara el diccionario serializado con `pickle`
    '''
    terms = {}
    index = 0
    max_frecs = []
    for doc in load(name_dataset).docs_iter():
        tokens = normalize(doc.text)
        frecs= nltk.FreqDist(tokens)
        for token, frec in frecs.items():
            dict_doc = terms.get(token, dict())
            dict_doc[index] = dict_doc.get(index,0) + frec
            terms[token] = dict_doc
        print(len(frecs.values()))
        max_frecs.append(1 if len(frecs) == 0 else max(frecs.values()))
        index+=1
        if index % 5000 == 0:
            print(index // 5000)

    idf = {}    
    for key in terms.keys():
        idf[key] = np.log( count_documents / len(terms[key]) )
    
    for key, value in terms.items():
        for doc, frec in value.items():
            terms[key][doc] = idf[key] * frec/max_frecs[doc]
    
    with open(destint_path, 'w') as tf:
        json.dump(terms, tf)


def create_numpy_lg(name_file, count_documents):
    '''
    Crea la matriz de terminos-documentos con pesos `l_i_j * g_i_j`.
    Necesita un diccionario de terminos-(documentos-frecuencia), que
    cargara de un directorio

    `name_file`: Nombre del archivo que contiene el diccionario
    `count_documents`: es la cantidad de documentos que tiene la coleccion sobre la que
    se conformo el diccionario
    '''

    with open(name_file, 'rb') as tf:
        d = json.load(tf)    
        #print(d)
    A = np.zeros((len(d.keys()), count_documents), dtype= np.float32)
    g = np.zeros((len(d.keys()),))
    gf = np.zeros((len(d.keys()),))
    df = np.zeros((len(d.keys()),))
    terms = list(d.keys())

    for i in range(len(df)):
        df[i] = len(d[terms[i]])

    for i in range(len(gf)):
        for doc, frec in d[terms[i]].items():
            gf[i] = gf[i] + frec
    

    for i in range(len(d.keys())):
        g[i] = 1
        maximun = max([item[1] for item in d[terms[i]].items()])
        for j, frec in d[terms[i]].items():
            p_i_j = frec/(gf[i] * maximun)
            g[i] += (p_i_j * np.log(p_i_j))/np.log(count_documents)
        #g[i] = np.log2(count_documents/(1+len(d[terms[i]])))

    for i in range(len(terms)):        
        maximun = max([item[1] for item in d[terms[i]].items()])
        for key, value in d[terms[i]].items():
            A[i][int(key)] = g[i] * np.log(value/maximun + 1)
    return A

def extract_Dk_Rq(A, k, name_file):
    '''
    Hace la reduccion de dimension de la matriz `A`, usando descompision SVD

    `A`: Matriz a reducir

    `k`: Dimension de reduccion

    `name_file`: Direccion donde se guardaran las matrices de documentos reducidas,
    y la matriz de reduccion de consultas
    '''
    T, S, Dt =  np.linalg.svd(A, full_matrices=False)
    del(A)
    Tk = T[:,0:k]
    Dtk = Dt[0:k,:]
    Sk = S[0:k]

    Sk_inv = np.copy(Sk)
    for i in range(len(Sk_inv)):
        Sk_inv[i] = 1/Sk[i]

    Rq = np.diag(Sk_inv).dot(Tk.T)
    print(Rq.shape)
    print(Dtk.shape)
    np.save(name_file + 'Rq', Rq)
    np.save(name_file + 'Dk', Dtk.T)

def extract_terms(name_file, destint_file):
    '''
    Extrae un diccionario de terminos-indice, basado en el diccionario
    de termino-(documento-frecuencia).
    Este diccionario tiene uso practico para hacer mapeos de terminos sobre arrays

    `name_file`: Nombre del archivo donde se encuentra
    el diccionario de terminos-(documentos-indice)

    `destint_file`: Nombre del directorio y archivo en el que se va a guardar el diccionario
    de terminos-indice
    '''
    with open(name_file, 'rb') as tf:
        d = json.load(tf) 
    keys = list(d.keys())
    del(d)
    d = {}
    for i, key in enumerate(keys):
        d[key] = i
    with open(destint_file, 'wb') as tf:
        pickle.dump(d,tf)

def extract_idf(name_file, destint_file, count_documents):
    '''
    Extrae un diccionario de terminos-idf, basado en el diccionario
    de termino-(documento-frecuencia).
    Este diccionario tiene uso practico para hacer mapeos de terminos sobre arrays

    `name_file`: Nombre del archivo donde se encuentra
    el diccionario de terminos-(documentos-indice)

    `destint_file`: Nombre del directorio y archivo en el que se va a guardar el diccionario
    de terminos-indice

    `count_documents`: Cantidad de documentos que tiene la coleccion
    '''
    with open(name_file, 'rb') as tf:
        d = json.load(tf)

    df = {}    
    for key in d.keys():
        df[key] = np.log( count_documents / len(d[key]) )
    with open(destint_file, 'wb') as tf:
        pickle.dump(df, tf)

#extract_frec('beir/arguana', 'procesed_data/beir/arguana/frec.json')
#A = create_numpy_lg('procesed_data/beir/arguana/frec.json', 8674)
##
#extract_Dk_Rq(A,250,'procesed_data/beir/arguana/')
#extract_terms('procesed_data/beir/arguana/frec.json', 'procesed_data/beir/arguana/terms.pkl')
#extract_idf('procesed_data/beir/arguana/frec.json', 'procesed_data/beir/arguana/idf.pkl', 1400)

#with open('procesed_data/beir/arguana/Dk.npy', 'rb') as tf:
#    print(np.load(tf).shape)
#with open('procesed_data/beir/arguana/Rq.npy', 'rb') as tf:
#    print(np.load(tf).shape)

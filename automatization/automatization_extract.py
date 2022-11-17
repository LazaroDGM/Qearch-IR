import regex as re
import ir_datasets
import json
from nltk import WordNetLemmatizer
import os

import processing as pre

datasets = [
    "beir/arguana",
    "beir/dbpedia-entity",
    "beir/fiqa",
    "beir/cqadupstack/android",
    "beir/cqadupstack/english",
    "beir/cqadupstack/gaming",
    "beir/cqadupstack/gis",
    "beir/cqadupstack/mathematica",
    "beir/cqadupstack/physics",
    "beir/cqadupstack/programmers",
    "beir/cqadupstack/stats",
    "beir/cqadupstack/tex",
    "beir/cqadupstack/unix",
    "beir/cqadupstack/webmasters",
    "beir/cqadupstack/wordpress",
]

def extract_occurrence(dataset, name_file, start, stop, id=0):
    occurrence={}
    for doc in dataset.docs_iter()[start: stop]:
        set_terms = pre.preproc01(doc[1])
        for item in set_terms:
            docs = occurrence.get(item, set())
            docs.add(id)
            occurrence[item] = docs.union(docs)
        id+=1

    for key in occurrence.keys():    
        occurrence[key] = list(occurrence[key])        

    with open(name_file, 'w') as file:
        json.dump(occurrence, file)

def extract_frequency(dataset, name_file, start, stop, id=0):
    frequency={}
    for doc in dataset.docs_iter()[start: stop]:
        terms_f = pre.preproc02(doc[1])
        for term in terms_f:
            if term not in frequency:
                frequency[term] = dict()     
            frequency[term][id] = frequency[term].get(id, 0) + terms_f[term]
            #frequency[item] = docs.union(docs)
        id+=1

    #for key in frequency.keys():    
    #    frequency[key] = list(frequency[key])        

    with open(name_file, 'w') as file:
        json.dump(frequency, file)

def extract_block(dataset, name_file, size_block, info):
    total = dataset.docs_count()
    start = 0
    part = 0
    while start < total:
        stop = start+size_block
        print('Extrayendo bloque: '+ str(part))
        if info == 'ocurrence':
            extract_occurrence(dataset, name_file+'.part' + str(part) + '.json', start, stop, start)
        elif info == 'frequency':
            extract_frequency(dataset, name_file+'.part' + str(part) + '.json', start, stop, start)
        start = stop
        part += 1
    print("Extracción completada")
    return part

def auto_extract(size_block, info, dataset, name, path_result):
    if dataset not in datasets:
        raise Exception('SubDataSet no encontrado')
    os.makedirs(path_result, exist_ok= True)
    path_result = path_result + '\\' + name
    print(path_result)
    dataset = ir_datasets.load(dataset)
    print('Inicio Extracción')
    extract_block(dataset, path_result, size_block, info)

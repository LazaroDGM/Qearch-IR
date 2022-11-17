import regex as re
import json
import os

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

def open_ocurrence(name_file):
    try:
        with open(name_file) as file:
            # Cargar su contenido y crear un diccionario
            datos = json.load(file)
            for key in datos:
                datos[key] = set(datos[key])
            return datos
    except:
        return None

def open_frequency(name_file):
    try:
        with open(name_file) as file:
            # Cargar su contenido y crear un diccionario
            datos = json.load(file)
            for key in datos:
                print(datos[key])
                break
            return datos
    except:
        return None

def join_blocks_absolute(name_files, path_file, join_file):
    joined = {}    
    for name_file in name_files:
        datos = open_ocurrence(path_file + '\\' + name_file)        
        print("Uniendo parte: " + str(re.match('.*\.part([\d])*\.json', name_file)))
        for key in datos.keys():
            joined[key] = joined.get(key, set()).union(datos[key])
    print("Bloques unidos. Comenzando guardado")
    for key in joined.keys():    
        joined[key] = list(joined[key])
    with open(join_file, 'w') as file:
        json.dump(joined, file)
    print("Guardado")
    #return joined 

def auto_join(mode, size_block, info_join, first_name, path_files, path_result):    
    os.makedirs(path_result, exist_ok= True)

    l_dir = os.listdir(path_files)
    print(l_dir)
    f_dir = list(filter(lambda file: re.match(f'{first_name}\.part[\d]*\.json', file) != None, l_dir))
    print(f_dir)
    total = len(f_dir)

    print('Inicio Unión')
    index = 0
    start = 0
    while start < total:  
        if mode == 'absolute':
            join_blocks_absolute(name_files= f_dir[start: start + size_block],
                                 path_file= path_files,
                                 join_file= path_result + f'\\{first_name}.join.part{index}.json')
        index += 1
        start += size_block
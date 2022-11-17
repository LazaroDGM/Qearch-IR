import sys
from os import path
import os
from automatization_extract import auto_extract
from automatization_join import auto_join
import regex as re
import math

datasets = {
    "beir/arguana" : 0,
    "beir/dbpedia-entity" : 0,
    "beir/fiqa" : 0,
    "beir/cqadupstack/android" : 0,
    "beir/cqadupstack/english" : 0,
    "beir/cqadupstack/gaming" : 0,
    "beir/cqadupstack/gis" : 0,
    "beir/cqadupstack/mathematica" : 0,
    "beir/cqadupstack/physics" : 0,
    "beir/cqadupstack/programmers" : 0,
    "beir/cqadupstack/stats" : 0,
    "beir/cqadupstack/tex" : 0,
    "beir/cqadupstack/unix" : 0,
    "beir/cqadupstack/webmasters" : 0,
    "beir/cqadupstack/wordpress" : 0,
    "20news-18828/alt.atheism" : 1,
    "20news-18828/comp.graphics" : 1,
    "20news-18828/comp.os.ms-windows.misc" : 1,
    "20news-18828/comp.sys.ibm.pc.hardware" : 1,
    "20news-18828/comp.sys.mac.hardware" : 1,
    "20news-18828/comp.windows.x" : 1,
    "20news-18828/misc.forsale" : 1,
    "20news-18828/rec.autos" : 1,
    "20news-18828/rec.motorcycles" : 1,
    "20news-18828/rec.sport.baseball" : 1,
    "20news-18828/rec.sport.hockey" : 1,
    "20news-18828/sci.crypt" : 1,
    "20news-18828/sci.electronics" : 1,
    "20news-18828/sci.med" : 1,
    "20news-18828/sci.space" : 1,
    "20news-18828/soc.religion.christian" : 1,
    "20news-18828/talk.politics.guns" : 1,
    "20news-18828/talk.politics.mideast" : 1,
    "20news-18828/talk.politics.misc" : 1,
    "20news-18828/talk.religion.misc" : 1,
}

print(sys.argv)

argv = iter(sys.argv)
arg = next(argv)
arg = next(argv)
if arg == 'extract':
    dataset = None
    size_block = 1000
    name = ''
    path_result = path.abspath(path.dirname(__file__))
    info_extract = None

    arg = next(argv)
    if arg == '-sb' or arg == '-sizeblock':
        arg = next(argv)
        size_block = int(arg)
        arg = next(argv)
    if arg in ['ocurrence', 'frequency']:
        info_extract = arg
    else:
        raise Exception('Bad Info Extract: ', info_extract)
    arg = next(argv)
    if arg in datasets.keys():
        dataset = arg
    else:
        raise Exception('Bad Dataset')
    arg = next(argv, None)
    if arg == '-n' or arg == '--name':
        arg = next(argv)
        name = arg
        arg = next(argv, None)
    if arg == '-p' or arg == '--path':
        arg = next(argv)
        path_result = arg
    elif arg == None:
        path_result += '\\' + dataset
    else:
        raise Exception('Malformed Expression')
    print('extract: ' + info_extract + '\n'
        + 'dataset: ' + dataset + '\n'
        + 'name: ' + name + '\n'
        + 'size blocks: ' + str(size_block) + '\n'
        + 'path: ' + path_result)
    auto_extract(size_block, info_extract, dataset, name, path_result)
elif arg == 'join':
    mode = 'absolute'
    size_block = 100
    info_join = 'ocurrence'    
    dataset = None
    first_name = ''
    path_files = path.abspath(path.dirname(__file__))
    path_result = path.abspath(path.dirname(__file__)) + '\\' + 'join'

    arg = next(argv)
    if arg == '-m' or arg == '--mode':
        arg = next(argv)
        if arg in ['absolute']:
            mode = arg
        else:
            raise Exception('Bad Mode')
        arg = next(argv)
    if arg == '-b' or arg == '--blocks':
        arg = next(argv)
        size_block = int(arg)
        arg = next(argv)
    if arg in ['ocurrence','frequency']:
        info_join = arg
    else:
        raise Exception('Bad Info Join')
    arg = next(argv, None)
    if arg != None:
        first_name = arg
        arg = next(argv, None)
        if arg != None:
            path_files = arg
            arg = next(argv, None)
            if arg != None:
                path_result = arg
                if next(argv, None) != None:
                    raise Exception('Malformed Expression')
            else:
                path_result = path_files + '\\' + 'join' 
    print('join: ' + info_join + '\n'
        + 'mode: ' + mode + '\n'
        + 'size blocks: ' + str(size_block) + '\n'
        + 'first name: ' + first_name + '\n'
        + 'path files: ' + path_files + '\n'
        + 'path result: ' + path_result)
    auto_join(mode, size_block, info_join, first_name, path_files, path_result)
elif arg == 'ls':
    path = next(argv, None)
    if path == None:
        l_dir = os.listdir()
    else:
        l_dir = os.listdir(path)
    print(l_dir)
elif arg == 'rename':
    path = next(argv, None)
    if path == None:
        l_dir = os.listdir()
    else:
        l_dir = os.listdir(path)
    print(l_dir)
    max = 0
    for dir in l_dir:
        match = re.findall('^.*\.part([\d]*)\.json', dir)        
        if len(match) > 0:                        
            num = len(match[0])
            if max < num:
                max = num
    for dir in l_dir:        
        match = re.findall('^(.*)\.part([\d]*)\.json', dir)
        print(match)
        if len(match) > 0:
            zero = ''
            count = max-len(match[0][1])
            for i in range(0, count):
                zero += '0'
            print(match[0][0]+'.part' + zero + match[0][1] + '.json')
            os.rename(path + '\\' + match[0][0]+'.part' + match[0][1] + '.json',
                    path + '\\' + match[0][0]+'.part' + zero + match[0][1] + '.json')
    #print(max)
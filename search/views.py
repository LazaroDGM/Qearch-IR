from django.shortcuts import render
import regex as re
from boolean.boolean_model import BooleanModel, datasets
import sys

model = BooleanModel('beir/cqadupstack/tex')

# Create your views here.
def Home(request):
    query = []
    count = 0    
    if 'name_dataset' in request.GET.keys():
        name_dataset = request.GET['name_dataset']
        if name_dataset != model.name_dataset and name_dataset != '':
            model.ModDataset(name_dataset)
    if 'search' in request.GET.keys():
        search = request.GET['search']
        if re.match('.*[\w\d~&\(\)|]+.*', search) != None:
            #query.append(search)
            query = model.SearchIndex(search)
            count = len(query)
            query = model.SearchTitleDocsByIndex(query[0:10])
    return render(request, 'home.html',
                    {'query': query,
                     'count': count,
                     'name_dataset': model.name_dataset})

def Datasets(request):
    return render(request, 'datasets.html',
                    {'names': list(datasets.keys()),
                     'count': len(datasets),
                     'name_dataset': model.name_dataset})
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json

# from .modelos.vectorial import VectorialModel
from .modelos.boolean_model import BooleanModel
from .modelos.vectorial_model import VectorialModel
from .modelos.document_loader import DocumentLoader, metadata
from .modelos.lsi_model import LSIModel
from .modelos.Levenshtain import Sugestion

# from .modelos.vectorial_model import VectorialModel

DIR = 'sriApp/procesed_data/'


# from .CasosDeUso import Catalogo

# Create your views here.
textosdemuestra = {"estupido corse": "este texto trata sobre una muchacha que por falta de aire debido a que utilizaba un corse en los annos 1894, sufrio una muerte por ahogamiento"}

document_loader = DocumentLoader()
document_loader.ModDataset('cranfield', DIR)
current_model = [BooleanModel(document_loader._name_dataset)]
model_index = [0]
active_model: [bool] = [False]*3

_temp_results = [[0]]

def Home(request):
    print("Home view")
    print(f'active_model: {active_model}')
    return render(request,'home.html', { 'active_model' : active_model})
    
def ChangeModel(request, model:int):
    print(f"ChangeModel view, model: {model}")

    if model == 0:
        current_model[0] = BooleanModel(document_loader._name_dataset)
    elif model == 1:
        current_model[0] = VectorialModel(document_loader._name_dataset)
    elif model == 2:
        current_model[0] = LSIModel(document_loader._name_dataset)
    active_model[model_index[0]] = False
    model_index[0] = model
    active_model.insert(model, True)
    return render(request,'home.html', { 'active_model' : active_model})
def ChangeCorpus(request):
    print(request.GET['corpusIndex'])
    corpus = list(metadata.keys())[int(request.GET['corpusIndex'])]
    document_loader.ModDataset(corpus, DIR)
    current_model[0] = BooleanModel(document_loader._name_dataset)
    current_model[0].ModDataset(corpus)
    return Home(request)

def SelectCorpus(request):
    corpuses = enumerate(list(metadata.keys()))
    return render(request, 'corpus.html', {"corpuses": corpuses})


def DocPreview(request):
    index = int(request.GET['docIndex'])

    text = document_loader.SearchDocByIndex(_temp_results[0][index])[1]
    return render(request, 'book.html', {"text": text})
def Search(request):
    query = request.GET['search']

    # print(f"query: {query}")
    # return HttpResponse(json.dumps(textosdemuestra), content_type = "application/json")
    # return JsonResponse(textosdemuestra)    
    
    
    print(f"query: {query}")

    docs_per_page = 12
    starting_i = 0 # docs_per_page * page
    ending_i = starting_i + docs_per_page
    try:
        results = current_model[0].SearchIndex(query)[starting_i:ending_i]
    except:
        print('aqui')
        return render(request, 'results.html', {"error": True})
    _temp_results[0] = results
    sugestion = ""
    if (model_index[0] == 1 or model_index[0] == 2) and len(results) <= 5: 
        sugestion = list(Sugestion(terms=document_loader.get_term_idf(), query=query).values())
    results_texts =  document_loader.SearchDescriptionDocsByIndex(results)
    print(f'results: {results}')
    print(f'results_texts: {results_texts}')
    return render(request, 'results.html', {"results": enumerate(results_texts[starting_i:ending_i]), "sugestion": sugestion, "error": False})
















def ArtWorkCatalog(request, room):
    # sri.urls:        path('catalog/<str:room>/', views.ArtWorkCatalog, name = "artworkcatalog"),
    pass
from django.urls import path, include 
from . import views 
from django.conf import settings

# from django.conf.urls.static import static 

urlpatterns = [
    path('', views.Home, name = "home"),
    path('search/', views.Search, name = "search"),
    path('model/<int:model>/', views.ChangeModel, name = "model"),
    path('changeCorpus/', views.ChangeCorpus, name = "changeCorpus"),
    path('selectCorpus/', views.SelectCorpus, name = "selectCorpus"),
    path('preview/', views.DocPreview, name = "preview"),
    # path('change_model<int:model>', views.Search, name = "vectorial"),
    # path('change_model<int:model>', views.Search, name = "probabilistico"),
    # path('services/', views.Services, name = "services"),
    # path('catalog/', views.RoomCatalog, name = "catalog"),
    # path('catalog/<str:room>/', views.ArtWorkCatalog, name = "artworkcatalog"),
    # path('contact/', views.ContactUs, name = "contact"),
    # path('docs/', views.Documentation, name = "docs"),
    
]

# urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
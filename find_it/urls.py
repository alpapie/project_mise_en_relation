from django.urls import path
from django.urls.resolvers import URLPattern
from .import views 

urlpatterns=[
    #cette route mene a l'index du site
    path('', views.index,name='index'),
    #cette route renvoi la page de registrement
    path('registre',views.formRegistre,name='registre')
]
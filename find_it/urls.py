from django.urls import path
from django.urls.resolvers import URLPattern
from .import views 

urlpatterns=[
    #cette route mene a l'index du site
    path('', views.index,name='index'),
    #cette route renvoi la page de registrement
    path('Formregistre',views.formRegistre,name='Formregistre'),
    path('formEP',views.form_treatment_EP,name='formTraitEP'),
    path('formTraitUtil',views.form_treatment_utilisateur,name='formTraitUtil'),
    path('espaceIT',views.espace_it,name='espaceIT'),

]
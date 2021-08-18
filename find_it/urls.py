from django.urls import path
from django.urls.resolvers import URLPattern
from .import views 

urlpatterns=[
    
    #cette route mene a l'index du site
    path('', views.index,name='index'),
    
    #cette route renvoi la page de registrement
    path('Formregistre',views.formRegistre,name='Formregistre'),
    
    #les route de traitement de formulaire
    path('formEP',views.form_treatment_EP,name='formTraitEP'),
    path('formTraitUtil',views.form_treatment_utilisateur,name='formTraitUtil'),
    
    #les routes de formulaire de connection
    path('connect_it',views.connect_it,name='connect_it'),
    #path('connect_ep',views.connect_EP,name='connect_EP'),

    #deconnection des utilisateur
    path('logout',views.deconnection,name='logout'),
    
    #route pour enregistrer un mission
    path('mission',views.mission_teatement,name='post_mission') ,
    
    
     #route pour l'envoie des donne r sur la page de l'espace
    path('espace_it',views.espace_info,name='espace') ,
    
    #route pour enregistrer des posts
    path('postuler',views.it_post,name='postuler_it') ,
    
    
    #route de gestion lors d'un clic sur un domaine
    path('domaine/<domaine_search>',views.dommaine,name='domaine') ,
    
]
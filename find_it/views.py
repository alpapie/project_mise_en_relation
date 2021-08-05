from django.shortcuts import render
from .models import *
from django.http import request

# Create your views here.


#se view traite l'index on recuper et on n'affiche quelle donne

def index(request):
    dommaine=['Developpement web','Developpement Mobile','Infographie','Multumedia ','reseau ','cybersecuriter'
                     ]
    missions=Mission.objects.all()
    return render(request,'index.html',{'dommaine': dommaine,'missions':missions})
#cette view revoi la page  registre.html
def formRegistre(request):
    return render(request,'registre.html')

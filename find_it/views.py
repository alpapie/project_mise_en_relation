from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import request
from django.contrib.auth.decorators import login_required
from .forms import ITform,Uform,PEform,pe_uform

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


#on s'occuppe du traitement des donnes de l'utilisateur 
def form_treatment_utilisateur(request):
    errormessage="remplisser tous les champs"
    
    if request.method=='POST':
        #on transfert les donnee au form
        it_form=ITform(request.POST,request.FILES)
        u_form=Uform(request.POST)
        
        
        #on verifie si les donne et les champs des form corresponde
        if it_form.is_valid() and u_form.is_valid():
            #on verifie si l'email n'existe pas deja
            email=request.POST['email']
            user=User.objects.filter(email=email)
            if not user.exists():
                
                #on sauvegarde ses donne
                user=u_form.save()
                #on enregistre lmot de passe
                user.set_password(user.password)
                #on enregistre le user
                user.save()
                #on passe les donne additionnel de l'it sanns l'enregisttrer
                itw = it_form.save(commit=False)
                #on passe le user pour enregistrer la clee etranger dan itworker
                itw.user = user
                itw.save()
                
                #on authenthifie l'itilisateur
                # userit = authenticate(email=user.email, password=user.password)
                
                # #on verifie si elle n'est pas vide
                # if userit is not None:
                #     if userit.is_active:
                #         #et on le connecte
                #         login(request,userit)
                return render(request,'espace.html',{'user':user})
            else:
                #si l'email existe on renvoie se message
                errormessage="l'email existe deja"
                return  render(request,'registre.html',{'errormessage':errormessage})
            
    errormessage=it_form.errors
    return  render(request,'registre.html',{'errormessage':errormessage})
    



#on s'occuppe du traitement des donnes de l'entreprise
def form_treatment_EP(request):
    errormessagePE="remplisser tous les champs"
    if request.method=='POST':
        #on transfert les donnee au form
        PE_form=PEform(request.POST,request.FILES)
        PEu_form=pe_uform(request.POST)
        
        #on verifie si les donne et les champs des form corresponde
        if PE_form.is_valid() and PEu_form.is_valid():
            #on verifie si l'email n'existe pas deja
            email=request.POST['email']
            user=User.objects.filter(email=email)
            if not user.exists():
                
                #on sauvegarde ses donne
                user=PEu_form.save()
                #on enregistre lmot de passe
                user.set_password(user.password)
                #on enregistre le user
                user.save()
                #on passe les donne addPEionnel de l'PE sanns l'enregisttrer
                PE_registe = PE_form.save(commit=False)
                #on passe le user pour enregistrer la clee etranger dan PEworker
                PE_registe.user = user
                PE_registe.save()
                
                #on authenthifie l'itilisateur
                # userit = authenticate(email=user.email, password=user.password)
                
                # #on verifie si elle n'est pas vide
                # if userit is not None:
                #     if userit.is_active:
                #         #et on le connecte
                #         login(request,userit)
                return render(request,'espace.html',{'user':user})
            else:
                #si l'email existe on renvoie se message
                errormessagePE="l'email existe deja"
                return  render(request,'registre.html',{'errormessage':errormessagePE})
            
        errormessagePE=PE_form.errors
    return  render(request,'registre.html',{'errormessage':errormessagePE})

#gestion de l'espace de l'IT
def espace(request):
    if request.method == 'POST':
        #on extrait les donnee
        username = request.POST['username']
        password = request.POST['password']
        #on authenthifie l'itilisateur
        user = authenticate(username=username, password=password)
        #on verifie si elle n'est pas vide
        if user is not None:
            if user.is_active:
                #et on le connecte
                login(request,user)
                return render(request,'espace.html',{'user':user})
    errormessage="non d'utilisateur ou mot de passe incorre"
    return  render(request,'registre.html',{'errormessage':errormessage})



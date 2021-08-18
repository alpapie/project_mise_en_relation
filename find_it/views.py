from django.core.checks.messages import Info
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import request
from django.contrib.auth.decorators import login_required
from .forms import ITform,Uform,PEform,pe_uform,Conect,missionForm,PostForm
from django.shortcuts import get_object_or_404
# Create your views here.


#se view traite l'index on recuper et on n'affiche quelle donne
def index(request):
    if request.user.is_authenticated:
        return redirect('espace')
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
            
            #on verifie si les mot de passe corresponde
            if request.POST['password']==request.POST['passwordverif']:
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
                    return redirect('connect_it')
                else:
                    #si l'email existe on renvoie se message
                    errormessage="l'email existe deja"
                    return  render(request,'registre.html',{'errormessage':errormessage})
            else:
                
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
            #on verifie si les mot de passe corresponde
            if request.POST['password']==request.POST['passwordverif']:
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
                    userit = authenticate(email=user.email, password=user.password)
                    
                    # #on verifie si elle n'est pas vide
                    # if userit is not None:
                    #     if userit.is_active:
                    #         #et on le connecte
                    #         login(request,userit)
                    return redirect('connect_it')
                else:
                    #si l'email existe on renvoie se message
                    errormessagePE="l'email existe deja"
                    return  render(request,'registre.html',{'errormessage':errormessagePE})
            else:
                 errormessagePE="les mot de passe ne corresponde pas"
        errormessagePE=PE_form.errors
    return  render(request,'registre.html',{'errormessage':errormessagePE})


# #gestion de l'espace de l'EP
# def connect_EP(request):
#     form_EP=Conect()
#     error='mot de passe ou identifiant incorrect'
#     if request.method == 'POST':
#         #on extrait les donnee
#         username = request.POST['username']
#         password = request.POST['password']
#         #on authenthifie l'itilisateur
#         user_EP = authenticate(username=username, password=password)
#         #on verifie si elle n'est pas vide
#         if user_EP is not None:
#             if user_EP.is_active:
#                 #et on le connecte
#                 login(request,user_EP)
#                 #on envoie les donner
#                 return redirect('espace')

#     return  render(request,'connection.html',{'form_EP':form_EP,'error':error})

#on authentifie et
def connect_it(request):
    error=''
    form_it=Conect()
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
                return redirect('espace')
        error='mot de passe ou identifiant incorrect'
    #si l'utilisateur n'est pas connecter on le renvoie au niveau du formulaire
    return render(request,'connection.html',{'form_it':form_it,'error':error})

#on deconnect le user
@login_required
def deconnection(request):
    logout(request)
    return redirect('index') 
#traitement des donner du formulaire de mission  
 
@login_required
def mission_teatement(request):
    error=''
    #on genere le formulaire
    form_mission=missionForm() 
    if request.method=='POST':
        mission_req=missionForm(request.POST)
        #on verifie si les donne son valide
        if mission_req.is_valid():
            mission=mission_req.save(commit=False)
            #on recupere l'id de l'entreprise
            id_user=request.user.id
            pe=EntrepriseParticulier.objects.get(user_id=id_user)
            #on verifie si c une entreprise
            if pe:
                mission.PE=pe
                mission.logo=pe
                mission.save()
                return redirect('espace')
            else:
                error="vous ete pas une entrepris vou n'avez pas le droit de faire des mission"
                return  render(request,'mission_register.html',{'form_mission':form_mission,'error':error})
        else:
            error=mission_req.errors
    return  render(request,'mission_register.html',{'form_mission':form_mission,'error':error})


#vue pour le venvoi des donne vers l'espace du user
@login_required
def espace_info(request):
    id_user=request.user.id
    try:
       pe_info=EntrepriseParticulier.objects.get(user_id=id_user)
    except EntrepriseParticulier.DoesNotExist:
       pe_info = None
    
    try:
        it_info=ItWorker.objects.get(user_id=id_user)
    except ItWorker.DoesNotExist:
      it_info= None
  
    if pe_info:
        info=pe_info
        return render(request,'Entreprise/espace.html',{'info':info})
    else:
        it_info=ItWorker.objects.get(user_id=id_user)
        info=it_info
        return render(request,'it_worker/espace.html',{'info':info})
    
@login_required
def it_post(request):
    post_form=PostForm()
    error="veiller renseigner tous les champs"
    if request.method=='POST':
        post=PostForm(request.POST)
        if post.is_valid():
            post.save()
            return redirect('espace')
        else:
            error=post.errors
    return render(request,'poste_rgister.html',{'post_form':post_form,'error':error})


#on fait un requet pour recuperer les poste du domaine cliquer
@login_required
def dommaine(request,domaine_search):
    if domaine_search:
        mission=Mission.objects.filter(domaine=domaine_search)
        
    pass
def Mes_post(request):
    pass
def mes_mission():
    pass
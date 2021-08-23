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

isPosted=False
#se view traite l'index on recuper et on n'affiche quelle donne
def index(request):
    if request.user.is_authenticated and request.user.is_superuser==0:
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
    return render(request,'connection.html',{'error':error})

#on deconnect le user
@login_required
def deconnection(request):
    logout(request)
    return redirect('index') 
#traitement des donner du formulaire de mission  
 
@login_required
def mission_teatement(request):
    error=''
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
                mission.logo=pe.logo
                mission.save()
                return redirect('espace')
            else:
                error="vous ete pas une entrepris vou n'avez pas le droit de faire des mission"
                return  render(request,'mission_register.html',{'form_mission':form_mission,'error':error})
        else:
            error=mission_req.errors
    return  render(request,'mission_register.html',{'error':error})


#vue pour le venvoi des donne vers l'espace du user ou de l'entreprise
@login_required
def espace_info(request):
    post=None
    if request.user.is_authenticated and request.user.is_superuser==0:
        id_user=request.user.id
        try:
            pe_info=EntrepriseParticulier.objects.get(user_id=id_user)
        except EntrepriseParticulier.DoesNotExist:
            pe_info = None
        try:
            it_info=ItWorker.objects.get(user_id=id_user)
        except ItWorker.DoesNotExist:
            it_info= None
    
        if  pe_info:
            info=pe_info
            peid=pe_info.id
            
            missions=Mission.objects.filter(PE_id=peid)
            
            return render(request,'Entreprise/espace.html',{'info':info,'missions':missions,})
        else :
            domaine=it_info.domaine
            missions=Mission.objects.filter(domaine=domaine)
            info=it_info
            posts= Postuler.objects.filter(itworker_id=it_info.id)
            for mission in missions:
                for post in posts:
                    if post.mission_id == mission.id :
                        mission.isPosted=1
            return render(request,'it_worker/espace.html',{'info':info,'missions':missions,'posts':posts})
    return render(request ,'registre.html')

@login_required
def it_post(request,mission_id):
    error=''
    if request.method=='POST':
        postula=PostForm(request.POST)
        
        if postula.is_valid():
            postula=postula.save(commit=False)
            it_worker=ItWorker.objects.get(user_id=request.user.id) 
            postula.itworker=it_worker
            mission=Mission.objects.get(id=mission_id)
            postula.mission=mission
            postula.save()
            mission.isPosted=1
            return redirect('espace')
        
        error=postula.errors
    return render(request,'poste_rgister.html',{'error':error})


#on fait un requet pour recuperer les poste du domaine cliquer
@login_required
def dommaine(request,domaine_search):
    if domaine_search:
        mission=Mission.objects.filter(domaine=domaine_search)
        
    pass
#envoyer du postula avec comme param id de la mission

@login_required   
def mespost(request,id_it):
   
    missions_post=Postuler.objects.select_related('mission').filter(itworker=id_it)
    return render(request ,'it_worker/mes-post.html',{'missions_post':missions_post})
@login_required 
def detail_posts(request,detail_id):
    a_poster=False
    mission=Mission.objects.get(id=detail_id)
    try:
        post=Postuler.objects.get(mission_id=mission.id)
    except Postuler.DoesNotExist:
        post = None
    if post!=None:
        a_poster=True
    return render(request,'it_worker/detail-post.html',{'mission':mission,'a_poster':a_poster})

@login_required 
def detail_mission(request,mission_id):
    mission=Mission.objects.get(id=mission_id)
    posts=Postuler.objects.select_related('itworker').filter(mission_id=mission_id)
    return render(request,'Entreprise/detail-mission.html',{'mission':mission,'posts':posts})
   
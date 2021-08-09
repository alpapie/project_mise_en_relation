from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User
from django.http import request
from .forms import ITform,Uform,PEform

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
    it_form=ITform
    it=ItWorker()
    if request.method=='POST':
        it_form=ITform(request.POST,request.FILES)
        
        u_form=Uform(request.POST)
        errormessage="pas mmal"
        if it_form.is_valid() and u_form.is_valid():
            errormessage="humm bien"
            user=u_form.save()
            user.set_password(user.password)
            user.save()
            itw = it_form.save(commit=False)
            itw.user = user
            errormessage="humm bien"
            if 'image' in request.FILES:
                itw.image=request.FILES['image']
            itw.save()
            return redirect('espaceIT')
    errormessage=it_form.errors
    return  render(request,'registre.html',{'errormessage':errormessage})
    



#on s'occuppe du traitement des donnes de l'entreprise
def form_treatment_EP(request):
     #on recupere l'ensemble des donne
    #on recupere l'ensemble des donne
    userIT=Uform(instance=request.user)
    newPE=PEform(instance=request.User.EntrepriseParticulier)
    
    if request.method=="POST" :
      
        userIT=Uform(request.POST,instance=request.user)
        newPE=PEform(request.POST,request.FILES,instance=request.User.EntrepriseParticulier)
        #on verifie les mot de passe
        if request.POST['password']!=request.POST['passwordverif']:
            errormessagepassword="les mot de passe ne sont pas identique"
            return render(request,'registre.html',{'errormessagepassword':errormessagepassword})
        #on verifie si l'email n'existe pas
        newit=ItWorker.objects.filter(email=request.POST['email'])
        if not newit.exists():
            if userIT.is_valid() and newPE.is_valid():
               # on enregistre les donnees
                userIT.save()
                newPE.save()
            return redirect('espaceIT')
        else:
            errormessageemail ="ce email existe deja"
            #on retourne au niveau du page de registe + le message d;erreur
            return render(request,'registre.html',{'errormessage':errormessageemail})

    #on retourne au niveau du page de registe + le message d;erreur
    errormessage="remplisser tous les champs"
    return  render(request,'registre.html',{'errormessage':errormessage})

#gestion de l'espace de l'IT
def espace_it(request):
    
    return render(request,'espace.html')


#gestion de l'espace de l EP
def espace_EP():
    
    return 
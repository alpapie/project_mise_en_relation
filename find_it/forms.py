from django import forms
from django.db import models
from django.db.models.fields import DecimalField
from django.forms import fields
from django.contrib.auth.models import User
from .models import ItWorker,Mission,Postuler,EntrepriseParticulier
from django.contrib.auth.forms import UserCreationForm


class Uform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']
        
class ITform(forms.ModelForm):
    class Meta:
       model=ItWorker
       fields=['domaine','image','competence','sexe','date_naissance','description','adresse','numero_telephone']
      

class PEform(forms.ModelForm):
    class Meta:
       model=EntrepriseParticulier
       fields=['nom','logo','description','adresse','domaine']


class pe_uform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']

class Conect(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']

class missionForm(forms.ModelForm): 
    class Meta:
        model=Mission
        fields=['domaine','intituler','date_fin','description','fourcette_prix','outils']       


class PostForm(forms.ModelForm): 
    class Meta:
        model=Postuler
        fields=['itworker','mission','description','prix',]              
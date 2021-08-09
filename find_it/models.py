    
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this

class EntrepriseParticulier(models.Model):
    # id_pe = models.IntegerField(db_column='ID_PE' ,)  # Field name made lowercase.
    user = models.OneToOneField(User, on_delete=models.CASCADE)#nom = models.CharField( max_length=254)  # Field name made lowercase.
    nom= models.CharField( max_length=254)  # Field name made lowercase.
    logo = models.ImageField(upload_to='uploadslogo',null=True) 
    description = models.CharField( max_length=254)  # Field name made lowercase.
    adresse = models.CharField( max_length=254, null=True)  # Field name made lowercase.
    #email = models.EmailField( max_length=256)  # Field name made lowercase.
    #password = models.CharField( max_length=256)  # Field name made lowercase.
    domaine = models.CharField(max_length=254,null=True)
    def __str__(self): 
      return self.user.username

class ItWorker(models.Model):
    # id_itworker = models.IntegerField(db_column='ID_ITWORKER')  # Field name made lowercase.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    domaine = models.CharField(max_length=254,null=True)
    competence = models.CharField(max_length=254)  # Field name made lowercase.
    sexe = models.CharField( max_length=254, null=True) 
    image = models.ImageField(upload_to='uploads',null=True) 
    date_naissance= models.DateField(null=True)  # Field name made lowercase.
    description = models.CharField( max_length=254, null=True)  # Field name made lowercase.
    adresse = models.CharField( max_length=254, null=True)  # Field name made lowercase.
    #email = models.EmailField(max_length=255, null=True)
    numero_telephone = models.CharField(max_length=20, null=True)
    def __str__(self): 
      return self.user.username
    #password = models.CharField(max_length=32) # Field name made lowercase.
    # @receiver(post_save, sender=User) #add this
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         ItWorker.objects.create(user=instance)
    # @receiver(post_save, sender=User) #add this
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.itworker.save()



class Mission(models.Model):
    # id_mission = models.IntegerField(db_column='ID_MISSION')  # Field name made lowercase.
    PE = models.ForeignKey(EntrepriseParticulier,on_delete=models.CASCADE)
    dommaine = models.CharField(max_length=254,null=True,choices=[('1','developement web'),('2','art grafique'),('3','developement mobile'),('4','cybersecuriter')])
    intituler = models.CharField( max_length=254, null=True)  # Field name made lowercase.
    date_debut = models.DateTimeField( auto_now_add=True)  # Field name made lowercase.
    date_fin = models.DateField( null=True)  # Field name made lowercase.
    description = models.CharField( max_length=254, null=True)  # Field name made lowercase.
    fourcette_prix = models.DecimalField( max_digits=8, decimal_places=0, null=True)  # Field name made lowercase.
    outils = models.TextField()  # Field name made lowercase.



class Postuler(models.Model):
    # id_postula = models.IntegerField()
    itworker = models.ForeignKey(ItWorker,on_delete=models.CASCADE)  # Field name made lowercase.
    mission = models.ForeignKey(Mission,on_delete=models.CASCADE)  # Field name made lowercase.
    prix = models.TextField(null=True)
    decription = models.TextField(null=True)  # Field name made lowercase.
    date_postula = models.DateTimeField()


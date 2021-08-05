from django.contrib import admin
from .models import ItWorker,Mission,Postuler,EntrepriseParticulier

# Register your models here.
admin.site.register(ItWorker)
admin.site.register(EntrepriseParticulier)
admin.site.register(Mission)
admin.site.register(Postuler)



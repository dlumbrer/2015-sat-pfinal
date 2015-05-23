from django.contrib import admin

# Register your models here.

from models import Actividades, UltimaActualizacion, Usuarios, Apuntada

admin.site.register(Actividades)
admin.site.register(UltimaActualizacion)
admin.site.register(Usuarios)
admin.site.register(Apuntada)

from django.db import models
# Create your models here.

class Actividades(models.Model):
    titulo = models.TextField()
    tipo = models.TextField()
    precio = models.TextField()
    anno = models.IntegerField()
    mes = models.IntegerField()
    dia = models.IntegerField()
    hora = models.TextField()
    duracion = models.TextField()
    url = models.TextField()
    lat = models.TextField()
    lon = models.TextField()
    lugar = models.TextField()
    distrito = models.TextField()
    masinfo = models.TextField()
    
class UltimaActualizacion(models.Model):
    ultima = models.TextField()
    
class Usuarios(models.Model):
    titulo = models.TextField()
    usuario = models.CharField(max_length=32)
    descripcion = models.TextField()
    css = models.TextField()
    
class Apuntada(models.Model):
    usuario = models.ForeignKey(Usuarios)
    fecha = models.TextField()
    actividad = models.ForeignKey(Actividades)
    

    

from django.db import models

# Create your models here.
class Muro(models.Model):
    nombre = models.CharField(max_length=50)
    decripcion = models.TextField
    whatsapp = models.TextField(max_length=10)
    instagram = models.TextField


    def __str__(self):
        return self.nombre
    


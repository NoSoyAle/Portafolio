from django.db import models

# Create your models here.

class Comentario(models.Model):
    idComentario = models.IntegerField
    comentario = models.TextField
    fechaComentario = models.DateField


class Publicacion(models.Model):
    idPublicacion = models.IntegerField
    idUsuario = models.ForeignKey
    titulo = models.TextField
    texto = models.TextField
    img = models.ImageField(null= false)

    def __str__(self):
        return self.idPublicacion
    


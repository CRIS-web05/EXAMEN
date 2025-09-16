from django.db import models
from django.contrib.auth.models import User

class Pelicula(models.Model):
    title = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    anio = models.PositiveIntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
        return f"{self.title} - {self.user.username}"

# Create your models here.

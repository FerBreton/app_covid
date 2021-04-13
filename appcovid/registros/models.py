from django.db import models

# Create your models here.

class Registro(models.Model):
    email = models.EmailField()
    timestamp_in = models.DateTimeField(auto_now_add=True)
    timestamp_out = models.DateField(blank=True, null=True)
    temperatura = models.FloatField(max_length=45)
    oxigenacion = models.IntegerField()
    estado = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.email
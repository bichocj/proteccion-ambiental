from django.db import models

class Entrada(models.Model):
	titulo = models.CharField(max_length = 100)
	texto = models.TextField(null = True, blank = True)
	archivo = models.FileField(upload_to = "archivos/", null = True, blank = True)
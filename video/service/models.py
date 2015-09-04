from django.db import models

# Create your models here.

class File(models.Model):
    hashinfo = models.CharField(primary_key=True,max_length=128)






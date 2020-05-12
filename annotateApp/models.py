from django.db import models

# Create your models here.

# annotateapp_image table in db 
class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos')

# annotateapp_data table in db
class Data(models.Model):
    place_id = models.IntegerField(blank=True, null=True)
    lat = models.CharField(max_length=255, blank=True, null=True)
    lon = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255)

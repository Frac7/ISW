from django.db import models
from django.utils import timezone


class Albergatore(models.Model):
    nome = models.CharField(max_length=15)
    cognome = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=15)


class Hotel(models.Model):
    proprietario=models.ForeignKey(Albergatore)


class Camera(models.Model):
    hotel=models.ForeignKey(Hotel)


class Prenotazione(models.Model):
    camera=models.ForeignKey(Camera)
from django.db import models
from django.utils import timezone


class Albergatore(models.Model):
    nome = models.CharField(max_length=15)
    cognome = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=15)

class Indirizzo(models.Model):
    via = models.CharField(max_length=15)
    numero = models.CharField(max_length=5)

class Hotel(models.Model):
    nome = models.CharField(max_length=15)
    descrizione = models.CharField(max_length=100)
    citta = models.CharField(max_length=15)
    indirizzo = models.ForeignKey(Indirizzo)
    proprietario = models.ForeignKey(Albergatore)

class Camera(models.Model):
    hotel=models.ForeignKey(Hotel)


class Prenotazione(models.Model):
    camera=models.ForeignKey(Camera)
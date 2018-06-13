from django.db import models
from django.utils import timezone


class Albergatore(models.Model):
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=32)

class Indirizzo(models.Model):
    via = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)

class Hotel(models.Model):
    nome = models.CharField(max_length=50)
    descrizione = models.TextField()
    citta = models.CharField(max_length=50)
    indirizzo = models.ForeignKey(Indirizzo)
    proprietario = models.ForeignKey(Albergatore)
class Camera(models.Model):
    hotel=models.ForeignKey(Hotel)


class Prenotazione(models.Model):
    camera=models.ForeignKey(Camera)
    utente=models.CharField(max_length=50)
    checkin=models.DateField()
    checkout=models.DateField()


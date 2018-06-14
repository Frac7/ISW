from django.db import models

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
    nome = models.IntegerField(max_length=2)
    postiLetto = models.IntegerField(default=1)
    servizi = models.ForeignKey(Servizio)
    hotel = models.ForeignKey(Hotel)

class Servizio(models.Model):
    nome = models.CharField(max_length=15)
    descrizioneServizio = models.TextField()

class Prenotazione(models.Model):
    camera=models.ForeignKey(Camera)
    utente=models.CharField(max_length=50)
    checkin=models.DateField()
    checkout=models.DateField()


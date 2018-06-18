#TODO: setters
from django.db import models
import django
from django.utils import timezone

class Albergatore(models.Model):
    nome = models.CharField(max_length=50,default="")
    cognome = models.CharField(max_length=50,default="")
    email = models.EmailField(max_length=50,default="")
    password = models.CharField(max_length=32,default="")
    @staticmethod
    def autorizzaAccesso():
        pass
    def listaHotel(self):
        pass
    def prenotazioniPerAlbergatore(self):
        pass

class Indirizzo(models.Model):
    via = models.CharField(max_length=50,default="")
    numero = models.CharField(max_length=5,default="")
    def __str__(self):
        return "%s, %s", self.via, self.numero

class Servizio(models.Model):
    nome = models.CharField(max_length=15,default="")
    descrizioneServizio = models.TextField(default="")
    def __str__(self):
        return "%s, %s", self.nome, self.descrizioneServizio

class Hotel(models.Model):
    nome = models.CharField(max_length=50,default="")
    descrizione = models.TextField(default="")
    citta = models.CharField(max_length=50,default="")
    indirizzo = models.ForeignKey(Indirizzo)
    proprietario = models.ForeignKey(Albergatore)
    def getNome(self):
        return self.nome
    def getDescrizione(self):
        return self.descrizione
    def getCitta(self):
        return self.citta
    def getIndirizzo(self):
        return self.indirizzo
    def getProprietario(self):
        return self.proprietario
    def listaCamere(self):
        return Camera.objects.filter(hotel=self)
    #TODO: aggiungi camera

class Camera(models.Model):
    numero = models.CharField(max_length=15,default="")
    postiLetto = models.IntegerField(default=1)
    servizi = models.ManyToManyField(Servizio, through="ServiziDisponibili",through_fields=("camera","servizio"))
    hotel = models.ForeignKey(Hotel)
    def disponibilitaCamera(self, da, a):
        pass
    def listaServizi(self): #restituisce la lista di servizi per la camera
        serviziPerCamera = []
        for servizio in ServiziDisponibili.objects.filter(camera=self.id):
            serviziPerCamera.append(Servizio.objects.filter(id=servizio.id))
        return serviziPerCamera

class ServiziDisponibili(models.Model):
    camera=models.ForeignKey(Camera)
    servizio=models.ForeignKey(Servizio)

class Prenotazione(models.Model):
    camera=models.ForeignKey(Camera)
    utente=models.CharField(max_length=50,default="")
    checkin=models.DateField(default=django.utils.timezone.now)
    checkout=models.DateField(default=django.utils.timezone.now)
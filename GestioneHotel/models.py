#TODO: getters
from django.db import models
import django
from django.utils import timezone

class Albergatore(models.Model):
    nome = models.CharField(max_length=50,default="")
    cognome = models.CharField(max_length=50,default="")
    email = models.EmailField(max_length=50,default="")
    password = models.CharField(max_length=32,default="")
    @staticmethod
    def autorizzaAccesso(email, password):
        for albergatore in Albergatore.objects.all():
            if email == albergatore.email and password == albergatore.password:
                return True
            else:
                return False

    def listaHotel(self):
        listaHotel = []
        for hotel in Hotel.objects.filter(proprietario=self.id):
            listaHotel.append(hotel)
        return listaHotel

    def prenotazioniPerAlbergatore(self):
        listaPrenotazioni=[]
        for prenotazione in Prenotazione.objects.all():
            if prenotazione.camera.hotel.proprietario == self.id:
                listaPrenotazioni.append(prenotazione)
        return listaPrenotazioni

    def __unicode__(self):
        return "%s, %s, %s" % (self.nome, self.cognome, self.email)

class Indirizzo(models.Model):
    via = models.CharField(max_length=50,default="")
    numero = models.CharField(max_length=5,default="")

    def __unicode__(self):
        return "%s, %s" % (self.via, self.numero)


class Servizio(models.Model):
    nome = models.CharField(max_length=15,default="")
    descrizioneServizio = models.TextField(default="")

    def __unicode__(self):
        return "%s: %s" % (self.nome, self.descrizioneServizio)

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

    def contaCamere(self):
        count = 0
        for camera in Camera.objects.all():
            if camera.hotel.__eq__(self):
                count += 1
        return count
    #TODO: aggiungi camera
    def __unicode__(self):
        return "%s, %s" % (self.nome, self.citta)


class Camera(models.Model):
    numero = models.CharField(max_length=15,default="")
    postiLetto = models.IntegerField(default=1)
    servizi = models.ManyToManyField(Servizio, through="ServiziDisponibili",through_fields=("camera","servizio"))
    hotel = models.ForeignKey(Hotel)
    def getNumero(self):
        return self.numero
    def getPostiLetto(self):
        return self.postiLetto
    def listaServizi(self):  # restituisce la lista di servizi per la camera
        serviziPerCamera = []
        for servizioDisponibile in ServiziDisponibili.objects.filter(camera=self.id):
            serviziPerCamera.append(Servizio.objects.filter(id=servizioDisponibile.servizio.id))
        return serviziPerCamera
    def getHotel(self):
        return self.hotel
    def disponibilitaCamera(self, da, a, false=None, true=None):
        # dovrei controllare la lista delle prenotazioni che hanno come camera, questa, e vedere se quest'ultima
        # e' libera in quel lasso di tempo - GIUSTO?
        # perche' altrimenti non capisco questa funzione => Date due prenotazioni questa funzione avrebbe da restituire
        # le date libere pre-prenotazioni, post-prenotazioni e in mezzo se non sono consecutive
        if self.da > Prenotazione(camera=self.id).checkout and self.a > Prenotazione(camera=self.id).checkout or self.da < Prenotazione(camera=self.id).checkin and self.a < Prenotazione(camera=self.id).checkin:
            return true
        else:
            return false
    def __unicode__(self):
        return "%s, %s" % (self.numero, self.hotel)

class ServiziDisponibili(models.Model):
    camera=models.ForeignKey(Camera)
    servizio=models.ForeignKey(Servizio)

    def __unicode__(self):
        return "%s: %s" % (self.camera, self.servizio)

class Prenotazione(models.Model):
    camera=models.ForeignKey(Camera)
    utente=models.CharField(max_length=50,default="")
    checkin=models.DateField(default=django.utils.timezone.now)
    checkout=models.DateField(default=django.utils.timezone.now)
    def __unicode__(self):
        return "%s: %s, %s - %s" % (self.camera, self.utente, self.checkin, self.checkout)
from django.contrib.auth.models import AbstractUser
from django.db import models
import django
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext as _

class Albergatore(AbstractUser): #Estende user django
    email = models.EmailField(_('email address'), unique=True)
    nome = models.CharField(max_length=50, default="")
    cognome = models.CharField(max_length=50, default="")
    #Lista degli Hotel di un Albergatore
    def listaHotel(self):
        listaHotel = []
        for hotel in Hotel.objects.filter(proprietario=self.id):
            listaHotel.append(hotel)
        return listaHotel
    #Lista delle prenotazioni effettuate sulle camere di un Hotel di uin albergatore
    def prenotazioniPerAlbergatore(self):
        listaPrenotazioni=[]
        for prenotazione in Prenotazione.objects.all():
            if prenotazione.camera.hotel.proprietario == self:
                listaPrenotazioni.append(prenotazione)
        return listaPrenotazioni

    def __unicode__(self):
        return "%s" % (self.email)

@receiver(pre_save, sender=Albergatore)
def aggiornamentoCampoEmail(instance, **kwargs):
    if instance.email == "":
        instance.email = instance.username

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

#Classe Hotel
class Hotel(models.Model):
    #Nome dell'hotel
    nome = models.CharField(max_length=50,default="")
    #Descrizione dell'hotel
    descrizione = models.TextField(default="")
    #Citta' in cui si trova l'hotel
    citta = models.CharField(max_length=50,default="")
    #Indirizzo in cui si trova l'hotel
    indirizzo = models.ForeignKey(Indirizzo)
    #Albergatore che possiede l'hotel
    proprietario = models.ForeignKey(Albergatore)
    #Lista delle camere presenti nell'hotel
    def listaCamere(self):
        return Camera.objects.filter(hotel=self)
    #Override stampa oggetto Hotel
    def __unicode__(self):
        #Nome hotel, citta' hotel
        return "%s, %s" % (self.nome, self.citta)


class Camera(models.Model):
    numero = models.CharField(max_length=15,default="")
    postiLetto = models.IntegerField(default=1)
    servizi = models.ManyToManyField(Servizio, through="ServiziDisponibili",through_fields=("camera","servizio"))
    hotel = models.ForeignKey(Hotel)

    def listaServizi(self):
        serviziPerCamera = []
        for servizioDisponibile in ServiziDisponibili.objects.filter(camera=self.id):
            serviziPerCamera.append(Servizio.objects.filter(id=servizioDisponibile.servizio.id))
        return serviziPerCamera

    def disponibilitaCamera(self, da, a):
        listaPrenotazioniPerCamera = Prenotazione.objects.filter(camera=self)
        for prenotazione in listaPrenotazioniPerCamera:
            #Si controlla che la data da sia fuori dall'intervallo di prenotazione
            if prenotazione.checkin <= da and prenotazione.checkout >= da:
                return False
            #Si controlla che la data a sia fuori dall'intervallo di prenotazione
            if prenotazione.checkin <= a and prenotazione.checkout >= a:
                return False
            #Si controlla che la data da e la data a non si sovrappongano all'intervallo
            if da <= prenotazione.checkin and a >= prenotazione.checkout:
                return False
        return True

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
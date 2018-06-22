from django.db import models
import django
from django.utils import timezone

class Albergatore(models.Model):
    nome = models.CharField(max_length=50,default="")
    cognome = models.CharField(max_length=50,default="")
    email = models.EmailField(max_length=50,default="")
    password = models.CharField(max_length=32,default="")

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
            if not(da.year > prenotazione.checkout.year and a.year > Prenotazione(camera=self).checkout.year and da.month > prenotazione.checkout.month and a.month > prenotazione.checkout.month and da.day > prenotazione.checkout.day and a.day > prenotazione.checkout.day or da.year < prenotazione.checkin.year and a.year < prenotazione.checkin.year and da.month < prenotazione.checkin.month and a.month < prenotazione.checkin.month and da.day < prenotazione.checkin.day and a.day < prenotazione.checkin.day):
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
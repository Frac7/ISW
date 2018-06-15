#Test di accettazione per user story aggiungi camera
from GestioneHotel.models import *
from django.test import TestCase
import unittest

class TestAggiungiCamera(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "username@dominio"
        password = "unaPassword"
        self.albergatore = Albergatore(nome="un", cognome="Albergatore", email=email, password=password)
        self.albergatore.save()
        # Creazione singolo servizio: nome e descrizione
        servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        servizio.save()
        # Indirizzo hotel
        indirizzo = Indirizzo(via="Via Ospedale", numero="72")
        indirizzo.save()
        # Hotel in cui e' presente la camera
        self.hotel = Hotel(nome="unHotel", descrizione="unHotelACagliari", citta="Cagliari", indirizzo=indirizzo, proprietario=self.albergatore)
        self.hotel.save()
        # crea una camera con dei dati
        # Camera(numero, posti letto, servizi, hotel)
        self.camera = Camera(numero=1, postiLetto=4, hotel=self.hotel)
        self.camera.save()
        # Servizi a disposizione per la camera
        servizi = ServiziDisponibili(camera=self.camera, servizio=servizio)
        servizi.save()
    #Task login user story, requisito
    def testLogin(self):
        #Controlla che i dati inseriti siano validi per il login
        tuttiGliAlbergatori = Albergatore.objects.all()
        self.assertEqual(self.albergatore.email, tuttiGliAlbergatori.get(id=self.albergatore.id).email)
        self.assertEqual(self.albergatore.password, tuttiGliAlbergatori.get(id=self.albergatore.id).password)
    #task aggiungi camera, requisito user story
    def testAggiungiCamera(self):
        #Una volta creata la camera, si controlla che questa sia presente nell'hotel
        camera = Camera.objects.all().get(id=self.camera.id)
        self.assertEqual(camera.hotel, self.hotel, "Camera non aggiunta")

if __name__ == "__main__":
    unittest.main()

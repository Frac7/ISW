#Test unitario classe Hotel
from GestioneHotel.models import *
from django.test import TestCase
import unittest

class TestHotel(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "username@dominio"
        password = "unaPassword"
        albergatore = Albergatore(nome="un", cognome="Albergatore", email=email, password=password)
        albergatore.save()
        # Creazione singolo servizio: nome e descrizione
        servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        servizio.save()
        # Indirizzo hotel
        indirizzo = Indirizzo(via="Via Ospedale", numero="72")
        indirizzo.save()
        # Hotel in cui e' presente la camera
        self.hotel = Hotel(nome="unHotel", descrizione="unHotelACagliari", citta="Cagliari", indirizzo=indirizzo, proprietario=albergatore)
        self.hotel.save()
        # crea una camera con dei dati
        # Camera(numero, posti letto, servizi, hotel)
        self.camera = Camera(numero=1, postiLetto=4, hotel=self.hotel)
        self.camera.save()
        #Servizi a disposizione per la camera
        servizi = ServiziDisponibili(camera=self.camera, servizio=servizio)
        servizi.save()
    def testListaCamere(self):
        camera = Camera.objects.all().get(id=self.camera.id)
        self.assertEqual(camera.hotel, self.hotel, "Camera non aggiunta")
        self.assertEqual(len(Camera.objects.all()), 1, "La lunghezza della lista camera e\' diversa da 1")

if __name__ == "__main__":
    unittest.main()



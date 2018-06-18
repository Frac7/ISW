from django.test import TestCase
from datetime import date
import unittest

from GestioneHotel.models import Albergatore, Indirizzo, Hotel, Servizio, Camera, Prenotazione, ServiziDisponibili


class TestPrenotaCamera(TestCase):
    def setUp(self):
        self.albergatore = Albergatore(nome='Franco', cognome='Pischedda', email='piscofranco@gmail.com',
                                       password='password')
        self.albergatore.save()
        indirizzo = Indirizzo(via='Via Trincea Dei razzi', numero='152A')
        indirizzo.save()
        hotel = Hotel(nome='GrandRoyalHotel', descrizione='Hotel piu\' bello di Casteddu', citta='Cagliari',
                           indirizzo=indirizzo, proprietario=self.albergatore)
        hotel.save()


        camera = Camera(numero=1 ,postiLetto=4, hotel=hotel)
        camera.save()

        servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        servizio.save()

        serviziotv = ServiziDisponibili(camera=camera, servizio=servizio)
        serviziotv.save()

        self.prenotazione = Prenotazione(utente='pippo@gmail.it',camera=camera,checkin=date(2011, 8, 10),
                                         checkout=date(2011, 8, 30))
        self.prenotazione.save()
    def testPrenotaCamera(self):
        self.assertTrue(self.prenotazione in self.albergatore.prenotazioniPerAlbergatore(), "Prenotazione non aggiunta")

if __name__ == "__main__":
    unittest.main()
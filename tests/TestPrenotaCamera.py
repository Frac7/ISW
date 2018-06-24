from django.test import TestCase
from datetime import date
import unittest

from django.test import TestCase
from datetime import date
import unittest

from GestioneHotel.models import Albergatore, Indirizzo, Hotel, Servizio, Camera, Prenotazione, ServiziDisponibili


class TestPrenotaCamera(TestCase):
    def setUp(self):
        #Definisco degli elementi utilizzati nel test di accettazione
        self.albergatore = Albergatore(nome='Franco', cognome='Pischedda', username="piscofranco@gmail.com",
                                       email='piscofranco@gmail.com',
                                       password='password')
        self.albergatore.save()
        indirizzo = Indirizzo(via='Via Trincea Dei razzi', numero='152A')
        indirizzo.save()
        hotel = Hotel(nome='GrandRoyalHotel', descrizione='Hotel piu\' bello di Casteddu', citta='Cagliari',
                           indirizzo=indirizzo, proprietario=self.albergatore)
        hotel.save()


        self.camera = Camera(numero=1 ,postiLetto=4, hotel=hotel)
        self.camera.save()

        servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        servizio.save()

        serviziotv = ServiziDisponibili(camera=self.camera, servizio=servizio)
        serviziotv.save()

        self.prenotazione = Prenotazione(utente='pippo@gmail.it',camera=self.camera,checkin=date(2011, 8, 10),
                                         checkout=date(2011, 8, 30))
        self.prenotazione.save()
    def testPrenotaCamera(self):
        self.assertTrue(self.prenotazione in self.albergatore.prenotazioniPerAlbergatore(), "Prenotazione non aggiunta") #controllo che la prenotazione sia stata aggiunta con successo
        self.assertEqual(self.prenotazione.camera, self.camera) #controllo che la camera prenotata sia quella corretta
        self.assertEqual(self.prenotazione.utente, 'pippo@gmail.it') #controllo che l'email sia corretta

if __name__ == "__main__":
    unittest.main()
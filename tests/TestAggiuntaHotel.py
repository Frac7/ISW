from GestioneHotel.models import Albergatore, Servizio, Indirizzo, Hotel, Camera
from django.test import TestCase
import unittest


class TestAggiuntaHotel(TestCase):
    def setUp(self):
        self.albergatore = Albergatore(nome='Franco', cognome='Pischedda', email='piscofranco@gmail.com',
                                       password='password')
        self.albergatore.save()
        indirizzo = Indirizzo(via='Via Trincea Dei razzi', numero='152A')
        indirizzo.save()
        self.hotel = Hotel(nome='GrandRoyalHotel', descrizione='Hotel piu\' bello di Casteddu', citta='Cagliari',
                           indirizzo=indirizzo, proprietario=self.albergatore)
        self.hotel.save()

    def testRegistrazione(self):
        # errore perche albergatore non e iterabile, da correggere
        self.assertEqual(self.albergatore.email, Albergatore.objects.get(self.albergatore).email)
        self.assertEqual(self.albergatore.password, Albergatore.objects.get(self.albergatore).password)

    def testAggiungiHotel(self):
        self.assertTrue(self.hotel in self.albergatore.listaHotel(), 'Hotel non aggiunta')


if __name__ == "__main__":
    unittest.main()

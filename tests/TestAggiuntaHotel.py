from GestioneHotel.models import *
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
        tuttiGliAlbergatori = Albergatore.objects.all()
        self.assertEqual(self.albergatore.email, tuttiGliAlbergatori.get(id=self.albergatore.id).email)
        self.assertEqual(self.albergatore.password, tuttiGliAlbergatori.get(id=self.albergatore.id).password)
        self.assertEqual(tuttiGliAlbergatori.get(id=self.albergatore.id), self.albergatore)
        #Ho risolto il problema prendendo prima tutti gli oggetti (all) e poi facendo get sulla lista specificando il parametro
        #ovvero l'id di self.albergatore (che viene assegnato in automatico)

    def testAggiungiHotel(self):
        self.assertTrue(self.hotel in self.albergatore.listaHotel(), 'Hotel non aggiunto')


if __name__ == "__main__":
    unittest.main()

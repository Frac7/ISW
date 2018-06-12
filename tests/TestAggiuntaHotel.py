from django.test import TestCase
from GestioneHotel.models import Albergatore


class TestAggiuntaHotel(TestCase):
    def testAggiungiHotel(self):
        albergatore = Albergatore('Franco','Pischedda', 'piscofranco@gmail.com', 'password')
        indirizzo= Indirizzo('Via Trincea Dei razzi', '152A')
        hotel= Hotel('GrandRoyalHotel', 'Hotel più bello di Casteddu','Cagliari', indirizzo,albergatore )
        assert hotel in Albergatore.ListaHotel()
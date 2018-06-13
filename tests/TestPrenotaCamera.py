from django.test import TestCase
from datetime import date

from GestioneHotel.models import Albergatore, Indirizzo, Hotel, Servizio, Camera, Prenotazione


class TestPrenotaCamera(TestCase):
    def testPrenotaCamera(self):
        albergatore = Albergatore('Franco', 'Pischedda', 'piscofranco@gmail.com', 'password')
        indirizzo = Indirizzo('Via Trincea Dei razzi', '152A')
        hotel = Hotel('GrandRoyalHotel', 'Hotel piu\' bello di Casteddu', 'Cagliari', indirizzo, albergatore)
        servizio = Servizio("TV", "televisione")
        servizi = []
        servizi.append(servizio)
        camera=Camera(1,4,servizi,hotel)
        prenotazione=Prenotazione('pippo@gmail.it',camera,date(2011,8,10), date(2011,8,30))

        assert prenotazione in Albergatore.PrenotazioniPerAlbergatore()
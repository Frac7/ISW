from django.test import TestCase

from GestioneHotel.models import Albergatore


class TestPrenotaCamera(TestCase):
    def testPrenotaCamera(self):
        albergatore = Albergatore('Franco', 'Pischedda', 'piscofranco@gmail.com', 'password')
        indirizzo = Indirizzo('Via Trincea Dei razzi', '152A')
        hotel = Hotel('GrandRoyalHotel', 'Hotel più bello di Casteddu', 'Cagliari', indirizzo, albergatore)
        servizio = Servizio("TV", "televisione")
        servizi = []
        servizi.append(servizio)
        camera=Camera(1,4,servizi,hotel)
        prentazione=Prenotazione('pippo@gmail.it',camera,10/08/11, 30/08/11)

        assert prenotazione in Albergatore.PrenotazioniPerAlbergatore()
from GestioneHotel.models import Albergatore, Servizio, Indirizzo, Hotel, Camera
from django.test import TestCase
import unittest

class TestHotel(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "username@dominio"
        password = "unaPassword"
        self.albergatore = Albergatore("un", "Albergatore", email, password)
        self.albergatore.save()
        # Creazione singolo servizio: nome e descrizione
        servizio = Servizio("TV", "televisione")
        servizio.save()
        # Servizi a disposizione per la camera
        servizi = []
        servizi.append(servizio)
        # Indirizzo hotel
        indirizzo = Indirizzo("Via Ospedale", "72")
        indirizzo.save()
        # Hotel in cui e' presente la camera
        self.hotel = Hotel("unHotel", "unHotelACagliari", "Cagliari", indirizzo, self.albergatore)
        self.hotel.save()
        # crea una camera con dei dati
        # Camera(numero, posti letto, servizi, hotel)
        self.camera = Camera(1, 4, servizi, self.hotel)
    def testListaCamere(self):
        self.assertContains(self.camera, self.hotel.listaCamere(), 'Camera non aggiunta')
        self.assertEqual(len(Camera.objects.all()), 1, 'La lunghezza della lista camera e\' diversa da 1')

if __name__ == "__main__":
    unittest.main()



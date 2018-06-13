from django.test import TestCase
import unittest
from GestioneHotel.models import *

class TestPrenotazioni(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        albergatore=Albergatore(nome="NomeAlbergatore",cognome="CognomeAlbergatore",email="email",password="password")
        albergatore.save()
        hotel=Hotel(nome="Hilton",descrizione="Il Migliore",citta="Cagliari",albergatore=albergatore)
        hotel.save()
        camera=Camera(hotel=hotel)
        camera.save()
        prenotazione=Prenotazione(camera=camera,utente="email@dominio")
        prenotazione.save()

    def testPrenotazione(self):
        self.assertEqual(len(Hotel.objects.all()), 1)

if __name__ == "__main__":
    unittest.main()



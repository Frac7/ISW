from django.test import TestCase
import unittest

class TestHotel(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "username@dominio"
        password = "unaPassword"
        albergatore = Albergatore("un", "Albergatore", email, password)
        self.albergatore = albergatore
        # Creazione singolo servizio: nome e descrizione
        servizio = Servizio("TV", "televisione")
        # Servizi a disposizione per la camera
        servizi = []
        servizi.append(servizio)
        # Indirizzo hotel
        indirizzo = Indirizzo("Via Ospedale", "72")
        # Hotel in cui e' presente la camera
        hotel = Hotel("unHotel", "unHotelACagliari", "Cagliari", indirizzo, albergatore)
        # crea una camera con dei dati
        # Camera(numero, posti letto, servizi, hotel)
        camera = Camera(1, 4, servizi, hotel)
        self.camera = camera
    def testListaCamere(self):
        self.assertTrue(self.camera in hotel.listaCamere(), 'Camera non aggiunta')
        self.assertEqual(len(Camera.objects.all()), 1, 'La lunghezza della lista camera e\' diversa da 1')
if __name__ == "__main__":
    unittest.main()



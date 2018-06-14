from GestioneHotel.models import Albergatore, Servizio, Indirizzo, Hotel, Camera
from django.test import TestCase
import unittest

class TestHotel(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "username@dominio"
        password = "unaPassword"
        albergatore = Albergatore(nome="un", cognome="Albergatore", email=email, password=password)
        albergatore.save()
        # Creazione singolo servizio: nome e descrizione
        servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        servizio.save()
        # Servizi a disposizione per la camera
        servizi = []
        servizi.append(servizio)
        # Indirizzo hotel
        indirizzo = Indirizzo(via="Via Ospedale", numero="72")
        indirizzo.save()
        # Hotel in cui e' presente la camera
        self.hotel = Hotel(nome="unHotel", descrizione="unHotelACagliari", citta="Cagliari", indirizzo=indirizzo, proprietario_id=albergatore.id)
        self.hotel.save()
        # crea una camera con dei dati
        # Camera(numero, posti letto, servizi, hotel)
        self.camera = Camera(numero=1, postiLetto=4, servizi_id=servizio.id, hotel_id=self.hotel.id)
        self.camera.save()
    def testListaCamere(self):
        self.assertContains(self.camera, self.hotel.listaCamere(), 'Camera non aggiunta')
        self.assertEqual(len(Camera.objects.all()), 1, 'La lunghezza della lista camera e\' diversa da 1')

if __name__ == "__main__":
    unittest.main()



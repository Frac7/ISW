# Test di Accettazione per la Uesr Story Elenco Camera
from django.test import TestCase
from GestioneHotel.models import *
import unittest

class TestElencoCamere(TestCase):
    def setUp(self):
        email = "user@email.com"
        password = "password"
        albergatore = Albergatore(nome="Pippo", cognome="Albergatore", email=email, password=password)
        albergatore.save()

        # Creazione indirizzi per gli hotel
        indirizzo1 = Indirizzo(via='Via Trieste', numero='14')
        indirizzo1.save()

        # Creazione degli Hotel e poi aggiunta alla lista
        hotel1 = Hotel(nome='Gold Hotel', descrizione='L\'Hotel piu\' adatto per la vostra permanenza e riposo.',
                           citta='Cagliari', indirizzo=indirizzo1, proprietario=albergatore)
        hotel1.save()

        # Creazione lista delle camere legate all'hotel dichiarato sopra
        self.listaCamere = []

        # Creazione servizi per i servizi disponibili
        servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        servizio.save()

        # Creazione delle camere che verranno mostrate nella lista delle camere di un dato Hotel
        self.camera1 = Camera(numero=1, postiLetto=4, hotel=hotel1)
        self.camera1.save()
        self.listaCamere.append(self.camera1)
        self.camera2 = Camera(numero=2, postiLetto=3, hotel=hotel1)
        self.camera2.save()
        self.listaCamere.append(self.camera2)

    def testListaCamere(self):
        self.assertEqual(len(Camera.objects.all()), 2)
        #I parametri creati e salvati nel db temporaneao (le due camere, lista camera non viene salvato)
        #vengono assegnati come parametri della classi per essere utilizzati all'interno di questo test
        self.assertEqual(self.listaCamere[0], self.camera1, "Camera 1 non e' presente nella lista")
        self.assertEqual(self.listaCamere[1], self.camera2, "Camera 2 non e' presente nella lista")

if __name__ == "__main__":
        unittest.main()
#Test unitario classe Camera
from datetime import date
from GestioneHotel.models import *
from django.test import TestCase, Client
import unittest

class TestCamera(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "user@email.com"
        password = "password"
        self.albergatore = Albergatore(nome="Pippo", cognome="Albergatore", email=email, password=password)
        self.albergatore.save()

        # Creazione indirizzi per gli hotel
        indirizzo1 = Indirizzo(via='Via Trieste', numero='14')
        indirizzo1.save()

        # creazione degli Hotel e poi aggiunta alla lista
        self.hotel1 = Hotel(nome='Gold Hotel', descrizione='L\'Hotel piu\' adatto per la vostra permanenza e riposo.',
                            citta='Cagliari',indirizzo=indirizzo1, proprietario=self.albergatore)
        self.hotel1.save()

        # Creazione servizi per i servizi disponibili
        self.servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        self.servizio.save()

        # Creazione delle camere
        self.camera1 = Camera(numero=1, postiLetto=4, hotel=self.hotel1)
        self.camera1.save()

        # Servizi a disposizione per la camera
        self.servizi = ServiziDisponibili(camera=self.camera1, servizio=self.servizio)
        self.servizi.save()

        # Creazione prenotazione camera
        self.prenotazione1 = Prenotazione(utente='utenteNonRegistrato1@gmail.it', camera=self.camera1,
                                          checkin=date(2012, 3, 15), checkout=date(2011, 8, 30))
        self.prenotazione1.save()

        # Creazione client per test richiesta/risposta
        self.client = Client()

    def testModelsListaServizi(self):
        servizi = ServiziDisponibili.objects.all().get(id=self.servizi.id)
        self.assertEqual(servizi.servizio, self.servizio, "Il servizio non e' stato aggiunto correttamente")
        self.assertEqual(len(Servizio.objects.all()), 1, "La lunghezza della lista dei servizi creati e' diversa da uno, e invece dovrebbe essere 1")
        self.assertEqual(len(servizi.camera.listaServizi()), 1, "La lunghezza della lista dei servizi creati e' diversa da uno, e invece dovrebbe essere 1")

    def testModelsDisponibilitaCamera(self):
        camera = Camera.objects.all().get(id=self.camera1.id)
        self.assertEqual(camera, self.camera1, "La creazione della camera1 non e' andata a buon fine")
        self.assertEqual(len(Prenotazione.objects.all()), 1, "La lunghezza della lista di prenotazioni e' diversa da uno, e invece dovrebbe essere 1")

    def testModelsCamera(self):
        self.assertEqual(len(Camera.objects.all()), 1, "La lunghezza della lista camere e' diversa da 1")
        camera2 = Camera(numero=2, postiLetto=4, hotel=self.hotel1)
        self.assertNotEqual(self.camera1, camera2, "E' la stessa camera, allora creazione della camera2 non e' andata a buon fine")
        self.assertNotEqual(self.prenotazione1.camera, camera2, "E' la stessa camera, allora creazione della camera2 non e' andata a buon fine")

if __name__ == "__main__":
    unittest.main()
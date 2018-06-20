# -*- coding: utf-8 -*-
from datetime import *
from django.db import models
from django.contrib.auth import authenticate
from django.test import TestCase, Client
from GestioneHotel.models import *
import unittest

# Test Unitari.

class ModelTest(TestCase):
    # Creazione di Un Hotel
    def setUp(self):
        albergatore1 = Albergatore(nome="Pino", cognome="Pipetta", email="pinopipetta@outlook.com", password="ninnito42")
        albergatore1.save()
        albergatore2 = Albergatore(nome="Pippo", cognome="Pluto", email="pippopluto@outlook.com", password="cosimo83")
        albergatore2.save()
        indirizzo = Indirizzo(via="Via Lombardia", numero="32")
        indirizzo.save()
        self.hotel1=Hotel(nome="Hilton", descrizione="Il Migliore!", citta="Cagliari", indirizzo=indirizzo, proprietario=albergatore1)
        self.hotel1.save()
        self.hotel2=Hotel(nome="Hilton", descrizione="Il Migliore!", citta="Roma", indirizzo=indirizzo, proprietario=albergatore2)
        self.hotel2.save()
    # Conteggio Hotels
    def testCountHotels(self):
        self.assertEqual(len(Hotel.objects.all()),2)

    def testCountAlbergatores(self):
        self.assertEqual(len(Albergatore.objects.all()), 2)

class TestPrenotazioni(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password)
        albergatore=Albergatore(nome="NomeAlbergatore",cognome="CognomeAlbergatore",email="email",password="password")
        # Salvataggio nel db temporaneo
        albergatore.save()

        # Creazione indirizzo (via, numero)
        indirizzo=Indirizzo(via="Via Berlino",numero="12")
        # Salvataggio nel db temporaneo
        indirizzo.save()

        # Creazione hotel (nome, descrizione, citta, proprietario, indirizzo)
        hotel=Hotel(nome="Hilton",descrizione="Il Migliore",citta="Cagliari",proprietario=albergatore,indirizzo=indirizzo)
        # Salvataggio nel db temporaneo
        hotel.save()

        # Creazione hotel (hotel, numero, postiletto)
        self.camera=Camera(hotel=hotel,numero=303,postiLetto=3)
        # Salvataggio nel db temporaneo
        self.camera.save()

        # Creazione servizio1 (nome, descrizioneservizio)
        tv=Servizio(nome="TV",descrizioneServizio="Satellitare")
        # Salvataggio nel db temporaneo
        tv.save()
        # Creazione servizio1 (nome, descrizioneservizio)
        fb=Servizio(nome="FB",descrizioneServizio="Frigo Bar")
        # Salvataggio nel db temporaneo
        fb.save()

        #Creazione servizio tv disponibile per la camera (camera,servizio)
        serviziotv=ServiziDisponibili(camera=self.camera,servizio=tv)
        # Salvataggio nel db temporaneo
        serviziotv.save()
        # Creazione servizio frigo bar disponibile per la camera (camera,servizio)
        serviziofb = ServiziDisponibili(camera=self.camera, servizio=fb)
        # Salvataggio nel db temporaneo
        serviziofb.save()

        # Creazione prenotazione della camera (camera, utente,checkin,checkout)
        self.prenotazione=Prenotazione(camera=self.camera,utente="email@dominio",checkin=datetime.now(),checkout=datetime.now())
        # Salvataggio nel db temporaneo
        self.prenotazione.save()

    def testPrenotazione(self):
        # Controlla che la prenotazione sia stata inserita
        self.assertEqual(len(Prenotazione.objects.all()), 1)
        prenotazione = Prenotazione.objects.all().get(id=self.prenotazione.id)
        # Controlla che l'utente della prenotazione sia quello corretto
        self.assertEqual(prenotazione.utente,"email@dominio")
        #Controlla che la camera della prenotazione sia quella corretta
        self.assertEqual(prenotazione.camera, self.camera)

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

        # Creazione lista delle camere legate all'hotel dichiarato sopra
        self.listaCamere = []

        # Creazione servizi per i servizi disponibili
        self.servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        self.servizio.save()

        # Creazione delle camere
        self.camera1 = Camera(numero=1, postiLetto=4, hotel=self.hotel1)
        self.camera1.save()
        self.listaCamere.append(self.camera1)
        self.camera2 = Camera(numero=2, postiLetto=3, hotel=self.hotel1)
        self.camera2.save()
        self.listaCamere.append(self.camera2)

        # Servizi a disposizione per la camera
        self.servizi = ServiziDisponibili(camera=self.camera1, servizio=self.servizio)
        self.servizi.save()

        # Creazione prenotazione camera
        self.prenotazione1 = Prenotazione(utente='utenteNonRegistrato1@gmail.it', camera=self.camera1,
                                          checkin=date(2012, 3, 15), checkout=date(2012, 8, 30))
        self.prenotazione1.save()
        self.prenotazione2 = Prenotazione(utente='untenteNonRegistrato2@gmail.it', camera=self.camera2,
                                          checkin=date(2012, 3, 8), checkout=date(2012, 8, 30))
        self.prenotazione2.save()

        # Creazione client per test richiesta/risposta
        self.client = Client()

    def testModelsListaServizi(self):
        servizi = ServiziDisponibili.objects.all().get(id=self.servizi.id)
        self.assertEqual(servizi.servizio, self.servizio, "Il servizio non e' stato aggiunto correttamente")
        self.assertEqual(len(Servizio.objects.all()), 1, "La lunghezza della lista dei servizi creati e' diversa da uno, e invece dovrebbe essere 1")
        self.assertEqual(len(servizi.camera.listaServizi()), 1, "La lunghezza della lista dei servizi creati e' diversa da uno, e invece dovrebbe essere 1")

    def testModelsDisponibilitaCamera(self):
        camera = Camera.objects.all().get(id=self.camera1.id)
        camera2 = Camera.objects.all().get(id=self.camera2.id)
        self.assertEqual(camera, self.camera1, "La creazione della camera1 non e' andata a buon fine")
        self.assertEqual(len(Prenotazione.objects.all()), 2, "La lunghezza della lista di prenotazioni e' diversa da uno, e invece dovrebbe essere 1")
        self.assertFalse(camera.disponibilitaCamera(date(2012, 3, 15), date(2012, 8, 30)), "Camera non e' prenotata, quindi la prenotazione non esiste")
        self.assertFalse(camera2.disponibilitaCamera(date(2012, 3, 8), date(2012, 8, 30)),
                        "Camera non e' prenotata, quindi la prenotazione non esiste")
        self.assertFalse(camera.disponibilitaCamera(date(2012, 3, 15), date(2012, 8, 30))
                    and camera2.disponibilitaCamera(date(2012, 3, 8),date(2012, 8, 30)),"Camera non e' prenotata, quindi la prenotazione non esiste")

    def testModelsCamera(self):
        self.assertEqual(len(Camera.objects.all()), 2, "La lunghezza della lista camere e' diversa da 2")
        camera2 = Camera(numero=2, postiLetto=4, hotel=self.hotel1)
        self.assertNotEqual(self.camera1, camera2, "E' la stessa camera, allora creazione della camera2 non e' andata a buon fine")
        self.assertNotEqual(self.prenotazione1.camera, camera2, "E' la stessa camera, allora creazione della camera2 non e' andata a buon fine")

    def testListaCamere(self):
        self.assertEqual(len(Camera.objects.all()), 2)
        #I parametri creati e salvati nel db temporaneao (le due camere, lista camera non viene salvato)
        #vengono assegnati come parametri della classi per essere utilizzati all'interno di questo test
        self.assertEqual(self.listaCamere[0], self.camera1, "Camera 1 non e' presente nella lista")
        self.assertEqual(self.listaCamere[1], self.camera2, "Camera 2 non e' presente nella lista")

class TestHotel(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "username@dominio"
        password = "unaPassword"
        self.albergatore = Albergatore(nome="un", cognome="Albergatore", email=email, password=password)
        self.albergatore.save()
        # Creazione singolo servizio: nome e descrizione
        servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        servizio.save()
        # Indirizzo hotel
        indirizzo = Indirizzo(via="Via Ospedale", numero="72")
        indirizzo.save()
        # Hotel in cui e' presente la camera
        self.hotel = Hotel(nome="unHotel", descrizione="unHotelACagliari", citta="Cagliari", indirizzo=indirizzo, proprietario=self.albergatore)
        self.hotel.save()
        # Crea una camera con dei dati
        # Camera(numero, posti letto, servizi, hotel)
        self.camera = Camera(numero=1, postiLetto=4, hotel=self.hotel)
        self.camera.save()
        #Servizi a disposizione per la camera
        servizi = ServiziDisponibili(camera=self.camera, servizio=servizio)
        servizi.save()
        #Creazione client per test richiesta/risposta
        self.client = Client()

    def testModelsListaCamere(self):
        #Test models (test con gli oggetti del DB)
        camera = Camera.objects.all().get(id=self.camera.id)
        self.assertEqual(camera.hotel, self.hotel, "Camera non aggiunta")
        self.assertEqual(len(Camera.objects.all()), 1, "La lunghezza della lista camera e\' diversa da 1")
        self.assertEqual(len(camera.hotel.listaCamere()), 1, "La lunghezza della lista camera e\' diversa da 1")
        self.assertEqual(Camera.objects.all().get(id=self.camera.id), Camera.objects.filter(hotel=self.hotel).get(id=self.camera.id))

    def testViewsListaCamere(self):
        #Per visualizzare la lista camere e' necessario loggarsi, si manda una richiesta POST con i dati
        response = self.client.post("/Login/", {"email": self.albergatore.email, "password": self.albergatore.password})
        self.assertTrue(response)
        #Visualizzazione pagina lista camere di un certo hotel
        response = self.client.get("/InfoHotelAggiungiCamera/" + self.hotel.id.__str__() +"/", follow=True)
        #Si controlla che la risposta contenga i dati delle camere
        self.assertContains(response, self.camera.numero)
        self.assertContains(response, self.camera.postiLetto)
        for servizi in self.camera.listaServizi():
            for servizio in servizi:
                self.assertContains(response, servizio.nome)
                self.assertContains(response, servizio.descrizioneServizio)
        self.assertNotContains(response, "WI-FI")

    def testViewsUtenteNonLoggato(self):
        response = self.client.get("/InfoHotelAggiungiCamera/" + self.hotel.id.__str__() +"/")
        self.assertEquals(response.status_code, 302)
        #Redirection (login e poi info hotel)
        self.assertEquals(response.url, "/Login?next=/InfoHotelAggiungiCamera/" + self.hotel.id.__str__() +"/")

    def testModelsHotel(self):
        self.assertEqual(len(Hotel.objects.all()), 1, "La lunghezza della lista hotel e\' diversa da 1")
        unAltroHotel = Hotel('unAltroHotel','unHotelDiversoDalPrecedente',"Roma",self.hotel.indirizzo,self.hotel.proprietario)
        self.assertNotEqual(self.hotel, unAltroHotel)
        self.assertNotEqual(self.camera.hotel, unAltroHotel)

    def testViewsHotel(self):
        response = self.client.post("/Login/", {"email": self.albergatore.email, "password": self.albergatore.password})
        self.assertTrue(response)
        response = self.client.get("/InfoHotelAggiungiCamera/" + self.hotel.id.__str__() + "/", follow=True)
        #Si controlla che la risposta contenga i dati dell'hotel
        self.assertContains(response, self.hotel.nome)
        self.assertContains(response, self.hotel.descrizione)
        self.assertContains(response, self.hotel.indirizzo.via)
        self.assertContains(response, self.hotel.indirizzo.numero)

    def testViewsAggiungiCamera(self):
        response = self.client.post("/Login/", {"email": self.albergatore.email, "password": self.albergatore.password})
        self.assertTrue(response)
        #Invio form
        response = self.client.post("/InfoHotelAggiungiCamera/" + self.hotel.id.__str__() + "/",
                                    {"numero": "101", "postiLetto": "1", "serivizio1": True, "serivizio2": False, "serivizio3": False }, follow=True)
        # Si controlla che la risposta contenga i dati della camera inserita
        self.assertContains(response, "101")
        self.assertContains(response, "1")

if __name__ == "__main__":
    unittest.main()


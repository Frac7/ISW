# -*- coding: utf-8 -*-
from datetime import *

from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import authenticate
from django.test import TestCase, Client
from GestioneHotel.models import *
import unittest

# Test Unitari.

class TestAlbergatore(TestCase):

    def setUp(self):
        email = "pinopipetta@outlook.com"
        self.password1 = "ninnito42"
        #Definisco degli elementi che salvo nel DB temporaneo per poter effettuare i test
        self.albergatore1 = Albergatore(nome="Pino", cognome="Pipetta", email=email, username=email)
        self.albergatore1.set_password(self.password1)
        self.albergatore1.save()
        self.password2 = "cosimo83"
        self.albergatore2 = Albergatore(nome="Pippo", cognome="Pluto", email="pippopluto@outlook.com", username="pippopluto@outlook.com")
        self.albergatore2.set_password(self.password2)
        self.albergatore2.save()
        self.password3 = "OrestinaSanna"
        self.albergatore3 = Albergatore(nome="Pasqualina", cognome="Nonnis", email="pasquaPesus@outlook.com", username="pasquaPesus@outlook.com")
        self.albergatore3.set_password(self.password3)
        self.albergatore3.save()
        indirizzo1 = Indirizzo(via="Via Trincea Delle Frasche", numero="13")
        indirizzo1.save()
        indirizzo2 = Indirizzo(via="Via Inferno", numero="667")
        indirizzo2.save()
        self.hotel1 = Hotel(nome="Park Rangers", descrizione="Chuck Norris Approved", citta="Cagliari", proprietario= self.albergatore1,
                      indirizzo=indirizzo1)
        self.hotel1.save()
        self.hotel2 = Hotel(nome="The Hell Resort", descrizione="Bello ma Brutto", citta="Gerusalemme",
                      proprietario=self.albergatore2,
                      indirizzo=indirizzo2)
        self.hotel2.save()
        self.camera = Camera(hotel=self.hotel1, numero=1408, postiLetto=2)
        self.camera.save()
        servizioTV = Servizio(nome="TV", descrizioneServizio="SKY")
        servizioTV.save()
        TVSky = ServiziDisponibili(camera=self.camera, servizio=servizioTV)
        TVSky.save()
        self.prenotazione = Prenotazione(camera=self.camera, utente="franchinodj@live.it", checkin=datetime.now(),
                                 checkout=datetime.now())
        self.prenotazione.save()
        self.client = Client()

    def testAlbergatore(self):
        self.assertEqual(len(Albergatore.objects.all()), 3) #controllo che gli albergatori siano 3
        self.assertEqual(self.albergatore1, self.hotel1.proprietario, "Albergatore assegnato in maniera errata") #controllo che l'hotel 1 abbia come albergatore albergatore1

    def testListaPrenotazioni(self):
        self.assertEqual(len(self.albergatore1.prenotazioniPerAlbergatore()), 1) #controllo che prenotazioni albergatore restituisca esattamente 1 elemento

    def testListaHotel(self):
        self.assertEqual(len(self.albergatore1.listaHotel()), 1) #controllo che lista hotel restituisca esattamente un solo elemento

    def testViewListaHotel(self): #qui il problema è che in setup non crei l'user django
        self.client.post("/Login/", {"email": self.albergatore1.email, "password": self.password1}, follow=True)
        response = self.client.post("/AggiungiHotel/" + str(self.albergatore1.id) + "/", follow=True)
        self.assertContains(response, self.hotel1.nome) #controllo che nella pagina ci sia il nome dell'hotel1

    def testViewListaPrenotazioni(self):
        self.client.post("/Login/", {"email": self.albergatore1.email, "password": self.password1}, follow=True)

        response = self.client.post("/Home/" + str(self.albergatore1.id), follow=True)
        self.assertContains(response, self.prenotazione.camera.numero) #controllo che nella pagina ci sia il numero della camera prenotata

    def testViewNessunaPrenotazione(self):
        #L'albergatore che cerca di accedere al suo hotel senza camera visualizza un messaggio apposito
        self.client.post("/Login/", {"email": self.albergatore2.email, "password": self.password2},
                         follow=True)
        response = self.client.get("/Home/" + str(self.albergatore2.id) + "/", follow=True)
        self.assertContains(response, "Ancora nessuna prenotazione")

    def testViewNessunHotel(self):
        #L'albergatore che cerca di accedere al suo hotel senza camera visualizza un messaggio apposito
        self.client.post("/Login/", {"email": self.albergatore3.email, "password": self.password3},
                         follow=True)
        response = self.client.get("/AggiungiHotel/" + str(self.albergatore2.id) + "/", follow=True)
        self.assertContains(response, "Ancora nessun hotel")

    def testViewsUtenteNonLoggato(self):
        #Un utente non loggato che cerca di accedere ai dettagli di un hotel deve prima effettuare l'accesso
        response = self.client.get("/AggiungiHotel/" + str(self.albergatore1.id) +"/")
        self.assertEquals(response.status_code, 302) #Redirezione
        self.assertEquals(response.url, "/Login?next=/AggiungiHotel/" + str(self.albergatore1.id) +"/")

    def testViewsUtenteNonTrovato(self):
        #Dopo aver effettuato l'accesso, l'utente tenta di accedere ad una pagina di un albergatore non esistente
        self.client.post("/Login/", {"email": self.albergatore1.email, "password": self.password1},
                         follow=True)
        response = self.client.post("/AggiungiHotel/" + str(0), follow=True)
        self.assertEqual(response.status_code, 404)

    def testViewsUtenteDiverso(self):
        # Dopo aver effettuato l'accesso, l'utente tenta di accedere ad una pagina di un altro albergatore
        self.client.post("/Login/", {"email": self.albergatore2.email, "password": self.password2},
                         follow=True)
        response = self.client.post("/AggiungiHotel/" + str(self.albergatore1.id) + "/", follow=True)
        #Redirezione: risposta, url attesa dopo il reindirizzamento, codice stato
        self.assertRedirects(response, "/AggiungiHotel/" + str(self.albergatore2.id) + "/", status_code=302)

    def testViewsAggiungiHotel(self):
        self.client.post("/Login/", {"email": self.albergatore2.email, "password": self.password2}, follow=True)
        response = self.client.post("/AggiungiHotel/" + str(self.albergatore2.id) + "/",
                                    {"nome": "Lu Hotel", "descrizione": "Hotel a 4 stelle a Carbonia", "citta": "Carbonia", "via": "Via Costituente", "numeroCivico": "30" }, follow=True)
        #Dopo aver effettuato il login e aggiunto un hotel con richiesta post, si controlla che questo sia presente
        for hotel in self.albergatore2.listaHotel():
            self.assertContains(response, hotel.nome)
            self.assertContains(response, len(hotel.listaCamere()))

    def testViewsAggiungiHotelFormErrato(self):
        numeroHotelPosseduti = len(self.albergatore2.listaHotel())
        self.client.post("/Login/", {"email": self.albergatore2.email, "password": self.password2}, follow=True)
        self.client.post("/AggiungiHotel/" + str(self.albergatore2.id) + "/",
                                    {}, follow=True)
        #Dopo aver effettuato il login e aggiunto un hotel con richiesta post errata, si controlla che questo non sia presente
        self.assertEqual(numeroHotelPosseduti, len(self.albergatore2.listaHotel()))
        self.client.post("/AggiungiHotel/" + str(self.albergatore2.id) + "/",
                                    {"nome": "hotel"}, follow=True)

class TestPrenotazioni(TestCase):

    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password)
        albergatore=Albergatore(nome="NomeAlbergatore",cognome="CognomeAlbergatore",email="email",username="email", password="password")
        # Salvataggio nel db temporaneo
        albergatore.save()

        # Creazione indirizzo (via, numero)
        self.indirizzo=Indirizzo(via="Via Berlino",numero="12")
        # Salvataggio nel db temporaneo
        self.indirizzo.save()


        self.citta="Cagliari"

        # Creazione hotel (nome, descrizione, citta, proprietario, indirizzo)
        self.hotel=Hotel(nome="Hilton",descrizione="Il Migliore",citta=self.citta,proprietario=albergatore,indirizzo=self.indirizzo)
        # Salvataggio nel db temporaneo
        self.hotel.save()

        # Creazione Camera (hotel, numero, postiletto)
        self.camera=Camera(hotel=self.hotel,numero=303,postiLetto=3)
        # Salvataggio nel db temporaneo
        self.camera.save()

        # Creazione servizio1 (nome, descrizioneservizio)
        self.tv=Servizio(nome="TV",descrizioneServizio="Satellitare")
        # Salvataggio nel db temporaneo
        self.tv.save()
        # Creazione servizio1 (nome, descrizioneservizio)
        self.fb=Servizio(nome="FB",descrizioneServizio="Frigo Bar")
        # Salvataggio nel db temporaneo
        self.fb.save()

        #Creazione servizio tv disponibile per la camera (camera,servizio)
        self.serviziotv=ServiziDisponibili(camera=self.camera,servizio=self.tv)
        # Salvataggio nel db temporaneo
        self.serviziotv.save()
        # Creazione servizio frigo bar disponibile per la camera (camera,servizio)
        self.serviziofb = ServiziDisponibili(camera=self.camera, servizio=self.fb)
        # Salvataggio nel db temporaneo
        self.serviziofb.save()

        # Creazione di un utente che prenota la camera
        self.utente = "email@dominio.com"

        # Imposto le date di checkin e checkout
        self.arrivo=date(2019,1,1)
        self.partenza=date(2019,1,10)
        # Creazione prenotazione della camera (camera, utente,checkin,checkout)
        self.prenotazione=Prenotazione(camera=self.camera,utente=self.utente,checkin=self.arrivo,checkout=self.partenza)
        # Salvataggio nel db temporaneo
        self.prenotazione.save()
        self.oggi=datetime.today()
        self.ieri=self.oggi - timedelta(days=1)
        # Inizializzazione del client
        self.client=Client()

    def testPrenotazione(self):
        # Controlla che la prenotazione sia stata inserita
        self.assertEqual(len(Prenotazione.objects.all()), 1)
        # seleziono la prenotazione salvata
        prenotazione = Prenotazione.objects.all().get(id=self.prenotazione.id)
        # Controlla che l'utente della prenotazione sia quello corretto
        self.assertEqual(prenotazione.utente,self.utente)
        #Controlla che la camera della prenotazione sia quella corretta
        self.assertEqual(prenotazione.camera, self.camera)
        # Controlla che l'hotel della prenotazione sia quello corretto
        self.assertEqual(prenotazione.camera.hotel, self.hotel)
        # Controlla che la data di checkin della prenotazione sia quella corretta
        self.assertEqual(prenotazione.checkin, self.arrivo)
        # Controlla che la data di checkout della prenotazione sia quella corretta
        self.assertEqual(prenotazione.checkout, self.partenza)

    def testViewsMainCameraTrovata(self):

        # Con date che non si sovrappongono a quelle in cui la camera è già stata prenotata
        response = self.client.post("/",{"citta": self.citta,
                "dataArrivo_day": 11,
                "dataArrivo_month": 1,
                "dataArrivo_year": 2019,
                "dataPartenza_day": 20,
                "dataPartenza_month": 1,
                "dataPartenza_year": 2019,
                "posti":self.camera.postiLetto})
        # Risposta HTTP Ok
        self.assertEqual(response.status_code,200)
        # Dopo aver effettuato la ricerca la pagina che risulta deve contenere  i dettagli della camera trovata:
        # Il nome dell'hotel
        self.assertContains(response, self.camera.hotel.nome)
        # Il numero della camera
        self.assertContains(response, self.camera.numero)
        # Il numero dei posti letto
        self.assertContains(response, self.camera.postiLetto)
        # Il nome dei servizi
        for servizi in self.camera.listaServizi():
            for servizio in servizi:
                self.assertContains(response, servizio.nome)

    def testViewsMainCameraOccupata(self):

        # Con date che si sovrappongono a quelle in cui la camera è già stata prenotata, nessuna camera deve essere trovata
        response = self.client.post("/",{"citta": self.citta,
                "dataArrivo_day": 9,
                "dataArrivo_month": 1,
                "dataArrivo_year": 2019,
                "dataPartenza_day": 20,
                "dataPartenza_month": 1,
                "dataPartenza_year": 2019,
                "posti":self.camera.postiLetto})
        # Risposta HTTP Ok
        self.assertEqual(response.status_code,200)
        # Dopo aver effettuato la ricerca la pagina che risulta deve contenere la stringa "Nessuna Camera Trovata":
        self.assertContains(response, "Nessuna Camera Trovata")

    def testViewsMainCameraDatePrecedentiAdOggi(self):

        # Con date non valide deve essere visualizzato un messaggio opportuno:
        # Nel caso in cui la data di arrivo o di partenza sia precedente alla data corrente:
        response = self.client.post("/",{"citta": self.citta,
                "dataArrivo_day": self.ieri.strftime("%d"),
                "dataArrivo_month": self.ieri.strftime("%m"),
                "dataArrivo_year": self.ieri.strftime("%Y"),
                "dataPartenza_day": self.oggi.strftime("%d"),
                "dataPartenza_month": self.oggi.strftime("%m"),
                "dataPartenza_year": self.oggi.strftime("%Y"),
                "posti":self.camera.postiLetto})
        # Risposta HTTP Ok
        self.assertEqual(response.status_code,200)
        # Dopo aver effettuato la ricerca la pagina che risulta deve contenere la stringa "non possono essere precedenti ad oggi":
        self.assertContains(response, "non possono essere precedenti ad oggi")

    def testViewsMainCameraDateNonCongrue(self):
        # Nel caso in cui la data di partenza sia precedente alla data di arrivo:
        fradiecigiorni=self.oggi + timedelta(days=10)
        response = self.client.post("/",{"citta": self.citta,
                "dataArrivo_day": fradiecigiorni.strftime("%d"),
                "dataArrivo_month": fradiecigiorni.strftime("%m"),
                "dataArrivo_year": fradiecigiorni.strftime("%Y"),
                "dataPartenza_day": self.oggi.strftime("%d"),
                "dataPartenza_month": self.oggi.strftime("%m"),
                "dataPartenza_year": self.oggi.strftime("%Y"),
                "posti":self.camera.postiLetto})
        # Risposta HTTP Ok
        self.assertEqual(response.status_code,200)
        # Dopo aver effettuato la ricerca la pagina che risulta deve contenere la stringa "la data di partenza deve essere successiva a quella di arrivo":
        self.assertContains(response, "la data di partenza deve essere successiva a quella di arrivo")


class TestCamera(TestCase):

    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "user@email.com"
        self.password = "password"
        self.albergatore = Albergatore(nome="Pippo", cognome="Albergatore", email=email, username=email)
        self.albergatore.set_password(self.password)
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
        self.client.logout()

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

    def testViewsCameraCreazioneServizi(self):
        self.assertTrue(len(Servizio.objects.all()), 0)
        #Si controlla che vengano generati i servizi di default durante la prima visualizzazione della lista camere
        self.client.post("/Login/", {"email": self.albergatore.email, "password": self.password}, follow=True)
        self.client.post("/InfoHotelAggiungiCamera/" + str(self.hotel1.id), follow=True)
        self.assertTrue(len(Servizio.objects.all()), 4)

    def testListaCamere(self):
        self.assertEqual(len(Camera.objects.all()), 2)
        #I parametri creati e salvati nel db temporaneao (le due camere, lista camera non viene salvato)
        #vengono assegnati come parametri della classi per essere utilizzati all'interno di questo test
        self.assertEqual(self.listaCamere[0], self.camera1, "Camera 1 non e' presente nella lista")
        self.assertEqual(self.listaCamere[1], self.camera2, "Camera 2 non e' presente nella lista")

class TestHotel(TestCase):

    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "username@dominio.it"
        self.password = "unaPassword"
        self.albergatore = Albergatore(nome="un", cognome="Albergatore", email=email, username=email)
        self.albergatore.set_password(self.password)
        self.albergatore.save()
        #Creazione altro user
        self.albergatore2 = Albergatore(nome="unNuovo", cognome="Albergatore", username="nuovoAlbergatore@email.com", email="nuovoAlbergatore@email.com")
        self.albergatore2.set_password(self.password)
        self.albergatore2.save()
        # Creazione singolo servizio: nome e descrizione
        servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        servizio.save()
        # Indirizzo hotel
        indirizzo = Indirizzo(via="Via Ospedale", numero="72")
        indirizzo.save()
        # Hotel in cui e' presente la camera
        self.hotel = Hotel(nome="unHotel", descrizione="unHotelACagliari", citta="Cagliari", indirizzo=indirizzo, proprietario=self.albergatore)
        self.hotel.save()
        #Un altro hotel da associare ad albergatore 2
        self.hotel2 = Hotel(nome="unAltroHotel", descrizione="unAltroHotelACagliari", citta="Cagliari", indirizzo=indirizzo,
                           proprietario=self.albergatore2)
        self.hotel2.save()
        # Crea una camera con dei dati
        # Camera(numero, posti letto, servizi, hotel)
        self.camera = Camera(numero=1, postiLetto=4, hotel=self.hotel)
        self.camera.save()
        #Servizi a disposizione per la camera
        servizi = ServiziDisponibili(camera=self.camera, servizio=servizio)
        servizi.save()
        #Creazione client per test richiesta/risposta
        self.client = Client()
        self.client.logout()

    def testModelsAggiungiCamera(self):
        #Recupera la camera creata
        camera = Camera.objects.all().get(id=self.camera.id)
        #Controlla che il campo camera dell'hotel sia uguale all'hotel in cui la camera è stata aggiunta
        self.assertEqual(camera.hotel, self.hotel, "Camera non aggiunta all'hotel")
        #Controlla che sia stata aggiunta la camera
        self.assertEqual(len(Camera.objects.all()), 1, "La lunghezza della lista camera e\' diversa da 1")
        #Controlla che la camera sia presente nell'hotel
        self.assertEqual(Camera.objects.all().get(id=self.camera.id), Camera.objects.filter(hotel=self.hotel).get(id=self.camera.id))
        hotel = Hotel(nome="unAltroHotel", descrizione="unAltroHotelACagliari", citta="Cagliari",
                      indirizzo=self.hotel.indirizzo, proprietario=self.albergatore)
        #Dopo aver creato un altro hotel, controlla che la camera non sia presente nel secondo
        self.assertNotEqual(self.camera.hotel, hotel)

    def testModelsListaCamere(self):
        #Controlla che lista camere restituisca il valore giusto
        self.assertEqual(len(self.hotel.listaCamere()), 1, "La lunghezza della lista camera e\' diversa da 1")
        hotel = Hotel(nome="unAltroHotel", descrizione="unAltroHotelACagliari", citta="Cagliari", indirizzo=self.hotel.indirizzo, proprietario=self.albergatore)
        self.assertEqual(len(hotel.listaCamere()), 0, "La lunghezza della lista camera e\' diversa da 0")
        #Dopo aver creato un altro hotel, controlla che non ci siano camere

    def testViewsUtenteNonLoggato(self):
        #Un utente non loggato che cerca di accedere ai dettagli di un hotel deve prima effettuare l'accesso
        response = self.client.get("/InfoHotelAggiungiCamera/" + str(self.hotel.id) +"/")
        self.assertEquals(response.status_code, 302) #Redirezione
        self.assertEquals(response.url, "/Login?next=/InfoHotelAggiungiCamera/" + str(self.hotel.id) +"/")

    def testViewsUtenteNonTrovato(self):
        #Dopo aver effettuato l'accesso, l'utente tenta di accedere ad una pagina di un hotel non esistente
        self.client.post("/Login/", {"email": self.albergatore.email, "password": self.password},
                         follow=True)
        response = self.client.post("/InfoHotelAggiungiCamera/" + str(0), follow=True)
        self.assertEqual(response.status_code, 404)

    def testViewsUtenteDiverso(self):
        # Dopo aver effettuato l'accesso, l'utente tenta di accedere ad una pagina di un hotel che non gli appartiene
        self.client.post("/Login/", {"email": self.albergatore.email, "password": self.password},
                         follow=True)
        response = self.client.post("/InfoHotelAggiungiCamera/" + str(self.hotel2.id) + "/", follow=True)
        #Redirezione: risposta, url attesa dopo il reindirizzamento, codice stato
        self.assertRedirects(response, "/Home/" + str(self.albergatore.id) + "/", status_code=302)

    def testViewsListaCamere(self):
        self.client.post("/Login/", {"email": self.albergatore.email, "password": self.password}, follow=True)
        response = self.client.post("/InfoHotelAggiungiCamera/" + str(self.hotel.id), follow=True)
        #Dopo aver effettuato il login ed aver mandato una richiesta get alla pagina del dettaglio hotel
        self.assertContains(response, self.camera.numero)
        self.assertContains(response, self.camera.postiLetto)
        for servizi in self.camera.listaServizi():
            for servizio in servizi:
                self.assertContains(response, servizio.nome)
                self.assertContains(response, servizio.descrizioneServizio)
        #Si controlla che la pagina contenga i dettagli delle camere dell'hotel

    def testModelsHotel(self):
        unAltroHotel = Hotel('unAltroHotel','unHotelDiversoDalPrecedente',"Roma",self.hotel.indirizzo,self.hotel.proprietario)
        #Si controlla che sia stato aggiunto un solo hotel
        self.assertEqual(len(Hotel.objects.all()), 2, "La lunghezza della lista hotel e\' diversa da 2")
        self.assertNotEqual(self.hotel, unAltroHotel)
        self.assertNotEqual(self.camera.hotel, unAltroHotel)
        #Si controlla, dopo la creazione di un nuovo hotel, che questo sia diverso dal precedente

    def testViewsHotel(self):
        self.client.post("/Login/", {"email": self.albergatore.email, "password": self.password}, follow=True)
        response = self.client.get("/InfoHotelAggiungiCamera/" + str(self.hotel.id) + "/", follow=True)
        #Dopo aver effettuato il login, si controlla che la pagina del dettaglio hotel contenga i dettagli dell'hotel
        self.assertContains(response, self.camera.numero)
        self.assertContains(response, self.hotel.nome)
        self.assertContains(response, self.hotel.descrizione)

    def testViewsAggiungiCamera(self):
        self.client.post("/Login/", {"email": self.albergatore.email, "password": self.password}, follow=True)
        response = self.client.post("/InfoHotelAggiungiCamera/" + str(self.hotel.id) + "/",
                                    {"numero": "101", "postiLetto": "1", "TV": True}, follow=True)
        #Dopo aver effettuato il login e aggiunto una camera con richiesta post, si controlla che questa sia presente
        self.assertContains(response, "101")
        self.assertContains(response, "1")
        self.assertContains(response, "TV")

    def testViewsAggiungiCameraFormErrato(self):
        numeroCamereHotel = len(self.hotel.listaCamere())
        self.client.post("/Login/", {"email": self.albergatore.email, "password": self.password}, follow=True)
        self.client.post("/InfoHotelAggiungiCamera/" + str(self.hotel.id) + "/",
                                    {}, follow=True)
        #Dopo aver effettuato il login e aggiunto una camera con richiesta post errata, si controlla che questa non sia presente
        self.assertEqual(numeroCamereHotel, len(self.hotel.listaCamere()))
        self.client.post("/InfoHotelAggiungiCamera/" + str(self.albergatore.id) + "/",
                         {"numero": 1}, follow=True)
        self.assertEqual(numeroCamereHotel, len(self.hotel.listaCamere()))

    def testViewNessunaCamera(self):
        #L'albergatore che cerca di accedere al suo hotel senza camera visualizza un messaggio apposito
        self.client.post("/Login/", {"email": self.albergatore2.email, "password": self.password},
                         follow=True)
        response = self.client.get("/InfoHotelAggiungiCamera/" + str(self.hotel2.id) + "/", follow=True)
        self.assertContains(response, "Ancora nessuna camera")

class TestLogin(TestCase):

    def setUp(self):
        #Creazione primo user
        #Creazione albergatore associato
        self.albergatore1 = Albergatore(email="albergatore@dominio.it", username="albergatore@dominio.it", nome="", cognome="")
        self.password1 = "UnaPasswordPerIlPrimoAlbergatore"
        self.albergatore1.set_password(self.password1)
        self.albergatore1.save()
        # Creazione altro user
        #Creazione albergatore associato
        self.albergatore2 = Albergatore(email="nuovoAlbergatore@email.com", username="nuovoAlbergatore@email.com", nome="", cognome="")
        self.password2 = "UnaPasswordPerIlSecondoAlbergatore"
        self.albergatore2.set_password(self.password2)
        self.albergatore2.save()
        #Creazione client
        self.client = Client()
        self.client.logout()

    def testLoginRiuscito(self):
        #Dopo essersi loggato, l'albergatore viene rimandato alla pagina delle sue prenotazioni
        response = self.client.post("/Login/", {"email": self.albergatore1.email, "password": self.password1}, follow=True)
        self.assertContains(response,"Qui, trovi le prenotazioni fatte ai tuoi Hotel.")

    def testEmailErrata(self):
        #Login con email errata: nella pagina deve essere mostrato un errore
        response = self.client.post("/Login/",
                                    {"email": "email@email.com", "password": self.password1},
                                    follow=True)
        self.assertContains(response, "I dati inseriti sono errati.")

    def testPasswordErrata(self):
        # Login con password errata: nella pagina deve essere mostrato un errore
        response = self.client.post("/Login/",
                                    {"email": self.albergatore1.email, "password": "p"},
                                    follow=True)
        self.assertContains(response, "I dati inseriti sono errati.")

    def testDatiErrati(self):
        # Login con email e password errati: nella pagina deve essere mostrato un errore
        response = self.client.post("/Login/",
                                    {"email": "email@email.com", "password": "p"},
                                    follow=True)
        self.assertContains(response, "I dati inseriti sono errati.")

    def testFormErrato(self):
        response = self.client.post("/Login/",
                                    {"email": "", "password": ""},
                                    follow=True)
        self.assertContains(response, "I dati inseriti sono errati.")

    def testVisualizzaMainLoggato(self):
        #Dopo aver effettuato l'accesso, l'albergatore non può visualizzare il main. Per prenotare deve sloggarsi
        self.client.post("/Login/",
                                    {"email": self.albergatore2.email, "password": self.password2},
                                    follow=True)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def testLoginLoggato(self):
        #Dopo aver effettuato l'accesso, l'albergatore non può visualizzare il login. Per accedere deve sloggarsi
        self.client.post("/Login/",
                                    {"email": self.albergatore2.email, "password": self.password2},
                                    follow=True)
        response = self.client.get("/Login/")
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/Login", follow=True)
        self.assertNotContains(response, "Welcome")

    def testVisualizzaHomeNonLoggato(self):
        #Un utente non loggato non può visualizzare la pagina delle prenotazioni
        response = self.client.get("/Home/" + str(self.albergatore1.id) + "/")
        self.assertEquals(response.url, "/Login?next=/Home/" + str(self.albergatore1.id) + "/")

    def testVisualizzaHotelNonLoggato(self):
        #Un utente non loggato non può visualizzare la pagina lista di hotel di un certo albergatore
        response = self.client.get("/AggiungiHotel/" + str(self.albergatore1.id) + "/")
        self.assertEquals(response.url, "/Login?next=/AggiungiHotel/" + str(self.albergatore1.id) + "/")

    def testVisualizzaCamereNonLoggato(self):
        # Un utente non loggato che cerca di accedere ai dettagli di un hotel deve prima effettuare l'accesso
        response = self.client.get("/InfoHotelAggiungiCamera/1/")
        self.assertEquals(response.url, "/Login?next=/InfoHotelAggiungiCamera/1/")

    def testLogout(self):
        self.client.post("/Login/",
                         {"email": self.albergatore2.email, "password": self.password2},
                         follow=True)
        response = self.client.get("/Logout/", follow=True)
        self.assertContains(response, "Tutti meritano una vacanza. Cosa aspetti?")
        #Si controlla che l'utente sia davvero sloggato, quindi si tenta di visualizzare la pagina delle prenotazioni
        response = self.client.get("/Home/" + str(self.albergatore1.id) + "/")
        self.assertEqual(response.status_code, 302)

    def testLogoutNonLoggato(self):
        #Un utente non loggato non può sloggarsi
        response = self.client.get("/Logout/")
        self.assertEquals(response.url, "/Login?next=/Logout/")

    def testViewsPrenotazioneLogin(self):
        # Un utente loggato che cerca di prenotare viene rimandato alla sua home
        self.client.post("/Login/",
                         {"email": self.albergatore1.email, "password": self.password1},
                         follow=True)
        response = self.client.post("/", {"citta": "Roma", "dataArrivo": "26-06-2018", "dataPartenza": "25-06-2018", "posti": 1}, follow=True)
        self.assertNotContains(response, "email")
        response = self.client.post("/Prenota/1/1/1/25-06-2018/26-06-2018/", {"email": "lol@email.com"}, follow=True)
        self.assertEqual(response.status_code, 404)

    def testRegistrazioneUtenteLoggato(self):
        #Un utente loggato che cerca di accedere alla registrazione viene rimandato alla sua home
        self.client.post("/Login/",
                         {"email": self.albergatore1.email, "password": self.password1},
                         follow=True)
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/Home/" + str(self.albergatore1.id))

class TestSignup(TestCase):
    def setUp(self):
        self.client=Client()
        self.client.logout()


    def testRegistrazioneOk(self):
        # L' Albergatore accede alla pagina signup e inserisce email, nome, cognome e le 2 password
        #  e viene riportato alla sua home
        nome="nome"
        cognome="Cognome"
        email="email@dominio.it"
        password1="thereception"
        password2 = "thereception"
        response = self.client.post("/signup/", {"username": email,
                    "nome": nome,
                    "cognome":cognome,
                    "password1":password1,
                    "password2":password2},
                    follow=True)
        self.assertContains(response,"Qui, trovi le prenotazioni fatte ai tuoi Hotel")


    def testUtenteNonInserito(self):
       nome = "nome"
       cognome = "Cognome"
       email = "email@dominio.it"
       password1 = "thereception"
       password2 = "thereception"
       response = self.client.post("/signup/", {"username": email,
                       "nome": "",
                       "cognome": "",
                       "password1": "",
                       "password2": ""},
                       follow=True)
       #Se la registrazione non va a buon fine, l'utente non deve vedere la home
       self.assertNotContains(response, "Prenotazioni")

    def testUtenteGiaPresente(self):
        # Il primo Albergatore accede alla pagina signup e inserisce email, nome, cognome
        #  e 2 volte la password
        nome="nome"
        cognome="Cognome"
        email="email@dominio.it"
        password1="thereception"
        password2 = "thereception"
        response = self.client.post("/signup/", {"username": email,
                    "nome": nome,
                    "cognome":cognome,
                    "password1":password1,
                    "password2":password2},
                    follow=True)
        #Una volta registrato l'utente deve vedere la sua home che ovviamente non avrà prenotazioni
        self.assertContains(response, "Ancora nessuna prenotazione...")
        response = self.client.get("/Logout/")
        # Un Secondo Albergatore, accede alla pagina signup e inserisce email già esistente
        # , nome, cognome e 2 volte la password
        response = self.client.post("/signup/", {"username": email,
                    "nome": nome,
                    "cognome":cognome,
                    "password1":password1,
                    "password2":password2},
                    follow=True)
        self.assertContains(response,"Un utente con questo nome è già presente")


    def testPasswordNonCorrispondenti(self):
        # L' Albergatore accede alla pagina signup e inserisce email, nome, cognome, password
        #  e la seconda password diversa dalla prima
        nome="nome"
        cognome="Cognome"
        email="email@dominio.it"
        password1="thereception1"
        password2 = "thereception2"
        response = self.client.post("/signup/", {"username": email,
                    "nome": nome,
                    "cognome":cognome,
                    "password1":password1,
                    "password2":password2},
                    follow=True)
        self.assertContains(response,"I due campi password non corrispondono.")


    def testPasswordTroppoComune(self):
        # L' Albergatore accede alla pagina signup e inserisce email, nome, cognome e
        #  una password troppo comune
        nome="nome"
        cognome="Cognome"
        email="email@dominio.it"
        password1="password"
        password2 = "password"
        response = self.client.post("/signup/", {"username": email,
                    "nome": nome,
                    "cognome":cognome,
                    "password1":password1,
                    "password2":password2},
                    follow=True)
        self.assertContains(response,"Questa password è troppo comune.")


    def testPasswordSoloNumerica(self):
        # L' Albergatore accede alla pagina signup e inserisce email, nome, cognome e
        #  una password interamente numerica
        nome="nome"
        cognome="Cognome"
        email="email@dominio.it"
        password1="12345678"
        password2 = "12345678"
        response = self.client.post("/signup/", {"username": email,
                    "nome": nome,
                    "cognome":cognome,
                    "password1":password1,
                    "password2":password2},
                    follow=True)
        self.assertContains(response,"Questa password è interamente numerica")

    def testRegistrazionePasswordTroppoCorta(self):
        response = self.client.post("/signup/", {
            "username": "albergatore@albergatore.it",
            "nome": "albergatore",
            "cognome": "cognome albergatore",
            "password1": "a1",
            "password2": "a1"
        }, follow=True)
        # La registrazione errata non deve riportare alla home
        self.assertNotContains(response, "I migliori hotel, pronti a proporti la loro camera per la tua vacanza.")
        self.assertContains(response, "Questa password è troppo corta")


    def testPasswordTroppoSimileANomeUtente(self):
        # L' Albergatore accede alla pagina signup e inserisce email, nome, cognome e
        #  una password troppo troppo simile al nome utente
        nome="nome"
        cognome="Cognome"
        email="email123@dominio.it"
        password1="email123"
        password2 = "email123"
        response = self.client.post("/signup/", {"username": email,
                    "nome": nome,
                    "cognome":cognome,
                    "password1":password1,
                    "password2":password2},
                    follow=True)
        self.assertContains(response,"La password è troppo simile a nome utente")


    def testPasswordNomeUtenteNonValido(self):
        # L' Albergatore accede alla pagina signup e inserisce una email non valida, nome, cognome e
        #  e le 2 password
        nome="nome"
        cognome="Cognome"
        email="email#@dominio.it"
        password1="thereception"
        password2 = "thereception"
        response = self.client.post("/signup/", {"username": email,
                    "nome": nome,
                    "cognome":cognome,
                    "password1":password1,
                    "password2":password2},
                    follow=True)
        self.assertContains(response,"Immetti un nome utente valido")

if __name__ == "__main__":
    unittest.main()
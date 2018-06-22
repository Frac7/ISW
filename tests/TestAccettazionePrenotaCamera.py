# -*- coding: utf-8 -*-
import unittest

from django.test import TestCase, Client
from GestioneHotel.models import *
from datetime import *

class TestAccettazionePrenotaCamera(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password)
        albergatore=Albergatore(nome="NomeAlbergatore",cognome="CognomeAlbergatore",email="email",password="password")
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
        self.camera=Camera(hotel=self.hotel,numero=303,postiLetto=4)
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

        # Inizializzazione del client
        self.client=Client()

    def testAccettazionePrenotazione(self):
        # L'utente ricerca una camera non prenotata con i parametri (città e posti letto)
        # della camera inserita
        response = self.client.post("/", {"citta": self.citta,
                                          "dataArrivo_day": 23,
                                          "dataArrivo_month": 12,
                                          "dataArrivo_year": 2018,
                                          "dataPartenza_day": 6,
                                          "dataPartenza_month": 1,
                                          "dataPartenza_year": 2019,
                                          "posti": 4})
        # Risposta HTTP Ok
        self.assertEqual(response.status_code, 200)
        # La pagina esito della ricerca  (ListaCamereDisponibili.htlm) deve contenere i dettagli dell'Hotel e della Camera
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

        # Sulla pagina di prenotazione, cliccando su prenota si va alla pagina Prenota.html
        # e da qui inserendo la mail dell'utente che prenota, e cliccando "Prenota" si deve registrare
        # la prenotazione e visualizzare la pagina di conferma


        response = self.client.post("/Prenota/Hilton/303/4/" + str(self.camera.id) + "/23-12-2018/6-1-2019/",
                    {"prenotaUtente": "unUtente@unDominio.com",
                     "prenotaCheckin":"23-12-2018",
                     "prenotaCheckout":"6-1-2019",
                     "prenotaIdCamera":self.camera.id})
        # Risposta HTTP Ok
        self.assertEqual(response.status_code, 200)
        # Se la pagina di conferma viene visualizzata
        self.assertContains(response, "Congratulazioni")

        # Controllo che la registrazione sia stata registrata
        prenotazione=Prenotazione.objects.all().filter(camera=self.camera,
                    utente="unUtente@unDominio.com",
                    checkin=date(2018,12,23),
                    checkout=date(2019,1,6))
        self.assertEqual(len(prenotazione),1)

if __name__ == "__main__":
    unittest.main()
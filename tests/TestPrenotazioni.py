from django.test import TestCase
import unittest
from GestioneHotel.models import *
from datetime import date,datetime

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

if __name__ == "__main__":
    unittest.main()



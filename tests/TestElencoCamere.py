# Test di Accettazione per la Uesr Story Elenco Camera
from django.test import TestCase
from GestioneHotel.models import *
import unittest

class TestElencoCamere(TestCase):
    def setUp(self):
        email = "user@email.com"
        password = "password"
        self.albergatore = Albergatore(nome="Pippo", cognome="Albergatore", email=email, password=password)
        self.albergatore.save()

        # Creazione indirizzi per gli hotel
        indirizzo1 = Indirizzo(via='Via Trieste', numero='14')
        indirizzo1.save()

        # Creazione degli Hotel e poi aggiunta alla lista
        self.hotel1 = Hotel(nome='Gold Hotel', descrizione='L\'Hotel piu\' adatto per la vostra permanenza e riposo.',
                           citta='Cagliari', indirizzo=indirizzo1, proprietario=self.albergatore)
        self.hotel1.save()

        # Creazione lista delle camere legate all'hotel dichiarato sopra
        self.listaCamere = []

        # Creazione servizi per i servizi disponibili
        servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        servizio.save()

        # Creazione delle camere che verranno mostrate nella lista delle camere di un dato Hotel
        self.camera1 = Camera(numero=1, postiLetto=4, hotel=self.hotel1)
        self.camera1.save()
        self.listaCamere.append(self.camera1)
        self.camera2 = Camera(numero=2, postiLetto=3, hotel=self.hotel1)
        self.camera2.save()
        self.listaCamere.append(self.camera2)

        ServiziDisponibili(camera=self.camera1,servizio=servizio).save()

    def testListaCamere(self):
        self.assertEqual(len(Camera.objects.all()), 2)
        #I parametri creati e salvati nel db temporaneao (le due camere, lista camera non viene salvato)
        #vengono assegnati come parametri della classi per essere utilizzati all'interno di questo test
        self.assertEqual(self.listaCamere[0], self.camera1, "Camera 1 non e' presente nella lista")
        self.assertEqual(self.listaCamere[1], self.camera2, "Camera 2 non e' presente nella lista")

    def testViewElencoCamere(self):
        # Per visualizzare la lista camere e' necessario loggarsi, si manda una richiesta POST con i dati
        response = self.client.post("/Login/", {"email": self.albergatore.email, "password": self.albergatore.password})
        self.assertTrue(response)
        response = self.client.get("/InfoHotelAggiungiCamera/" + self.hotel1.id.__str__() + "/", follow=True)

        # Si controlla che la risposta contenga i dati delle camere di un dato hotel posseduto dall'albergatore loggato
        self.assertContains(response, self.camera1.numero)
        self.assertContains(response, self.camera1.postiLetto)
        for servizi in self.camera1.listaServizi():
            for servizio in servizi:
                self.assertContains(response, servizio.nome)
                self.assertContains(response, servizio.descrizioneServizio)
            hotel = self.camera1.hotel
        #for hotel in self.camera1.hotel: #non iterabile
            self.assertContains(response, hotel.nome)
            self.assertContains(response, hotel.citta)
            #for hotel.indirizzo in self.camera1.hotel.indirizzo: #non iterabile
            self.assertContains(response, hotel.indirizzo.via)
            self.assertContains(response, hotel.indirizzo.numero)
            # NON SO SE IL FOR SOTTO SERVE, E SE SI, LI' E' DA FARE "CONTAINS" o "EQUAL"
            # PER CONTROLLARE IL PROPRIETARIO CON IL LOGIN (per questo c'e' il metodo autorizza accesso, comunque hai gia' fatto il login sopra con la POST)
            #for hotel.albergatore in self.camera1.hotel.proprietario: #non iterabile
                #self.assertContains(response, self.hotel.albergatore.nome)
                #self.assertContains(response, self.hotel.albergatore.cognome)

if __name__ == "__main__":
        unittest.main()
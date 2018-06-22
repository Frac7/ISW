# Test di Accettazione per la Uesr Story Elenco Camera
from django.test import TestCase, Client
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


        self.listaHotel = []

        # Creazione degli Hotel e poi aggiunta alla lista
        self.hotel1 = Hotel(nome='Gold Hotel', descrizione='L\'Hotel piu\' adatto per la vostra permanenza e riposo.',
                           citta='Cagliari', indirizzo=indirizzo1, proprietario=self.albergatore)
        self.hotel1.save()
        self.listaHotel.append(self.hotel1)



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

        # Creazione servizio all'interno di una camera esistente
        ServiziDisponibili(camera=self.camera1,servizio=servizio).save()

        # Creazione client
        self.client = Client()
        self.client.logout()

    def testListaCamere(self):
        self.assertEqual(len(Camera.objects.all()), 2)
        #I parametri creati e salvati nel db temporaneao (le due camere, lista camera non viene salvato)
        #vengono assegnati come parametri della classi per essere utilizzati all'interno di questo test
        self.assertEqual(self.listaCamere[0], self.camera1, "Camera 1 non e' presente nella lista")
        self.assertEqual(self.listaCamere[1], self.camera2, "Camera 2 non e' presente nella lista")

    def testViewElencoCamere(self):
        # Una volta fatto il login deve essere visualizzata la home
        self.client.post("/Login/",
                         {"email": self.albergatore.email, "password": self.albergatore.password},
                         follow=True)
        response = self.client.get("/InfoHotelAggiungiCamera/" + str(self.albergatore.id) + "/")

        # Si controlla che la risposta contenga i dati delle camere di un dato hotel posseduto dall'albergatore loggato
        self.assertContains(response, self.hotel1.nome)
        self.assertContains(response, len(self.hotel1.listaCamere()))
        self.assertContains(response, self.camera1.numero)
        self.assertContains(response, self.camera1.postiLetto)

        # Si itera su servizi di una data camera e se sono prenti, si controlla il nome e la descrizione
        for servizi in self.camera1.listaServizi():
            for servizio in servizi:
                self.assertContains(response, servizio.nome)
                self.assertContains(response, servizio.descrizioneServizio)
            hotel = self.camera1.hotel
            self.assertContains(response, hotel.nome)
            self.assertContains(response, hotel.citta)
            self.assertContains(response, hotel.indirizzo.via)
            self.assertContains(response, hotel.indirizzo.numero)


if __name__ == "__main__":
        unittest.main()
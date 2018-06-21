#test di accettazione per la user story, visualizza la lista prenotazioni
from django.test import TestCase, Client
from datetime import date
from GestioneHotel.models import *
import unittest

class TestListaPrenotazioni(TestCase):
    #task login user login, requisito
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
        self.hotel1 = Hotel(nome='Gold Hotel', descrizione='L\'Hotel piu\' adatto per la vostra permanenza e riposo.', citta='Cagliari', indirizzo=indirizzo1, proprietario=self.albergatore)
        self.hotel1.save()

        #Creazione servizi per i servizi disponibili
        servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        servizio.save()

        #Creazione delle camere che verranno mostrate nella lista delle prenotazioni in corso (che verranno mostrate nella lista all'albergatore)
        self.camera1 = Camera(numero=1, postiLetto=4, hotel=self.hotel1)
        self.camera1.save()
        self.camera2 = Camera(numero=2, postiLetto=3, hotel=self.hotel1)
        self.camera2.save()

        #Lego i servizi alle camere
        servizioTv = ServiziDisponibili(camera=self.camera1, servizio=servizio)
        servizioTv.save()
        servizioTv = ServiziDisponibili(camera=self.camera1, servizio=servizio)
        servizioTv.save()

        #Creazione lista delle prenotazioni che saranno visibili all'Albergatore in prima pagina, come si logga
        self.listaPrenotazioni = []


        #Creazione e aggiunta delle prenotazioni alla lista che verra mostrata all'Albergatore
        self.prenotazione1 = Prenotazione(utente='utenteNonRegistrato1@gmail.it', camera=self.camera1, checkin=date(2012, 3, 15),
                                     checkout=date(2011, 8, 30))
        self.prenotazione1.save()
        self.listaPrenotazioni.append(self.prenotazione1)
        self.prenotazione2 = Prenotazione(utente='untenteNonRegistrato2@gmail.it', camera=self.camera2, checkin=date(2012, 3, 8),
                                     checkout=date(2011, 8, 30))
        self.prenotazione2.save()
        self.listaPrenotazioni.append(self.prenotazione2)


        #assert Albergatore.autorizzaAccesso(albergatore.getEmail(), albergatore.getPassword())

    #Una volta loggato, l'utente accede dal menu alla lista delle prenotazioni che li mostra la lista delle prenotazioni
    #                   con i dati relativi ad ogni prenotazione

        self.client = Client() #inizializzazione client (vedi documentazione django, testing client)

    def testListaPrenotazioni(self):
        self.assertEqual(len(Prenotazione.objects.all()), 2)
        self.assertEqual(self.listaPrenotazioni[0], self.prenotazione1, "Prenotazione 1 non e' presente nella lista")
        self.assertEqual(self.listaPrenotazioni[1], self.prenotazione2, "Prenotazione 2 non e' presente nella lista")

    def testViewListaPrenotazioni(self):
        # Per visualizzare la lista camere e' necessario loggarsi, si manda una richiesta POST con i dati
        response = self.client.post("/Login/", {"email": self.albergatore.email, "password": self.albergatore.password}, follow=True)
        self.assertTrue(response)
        response = self.client.get("/Home/" + str(self.albergatore.id) + "/", follow=True)

        # Si controlla che la risposta contenga i dati degli delle prenotazioni, fatte agli hotel dell'albergatore loggato
        self.assertContains(response, self.prenotazione1.utente)
        #il template specifica solo numero e hotel
        self.assertContains(response, self.prenotazione1.camera.numero)
        self.assertContains(response, self.prenotazione1.camera.hotel.nome)
        #per ora ho aggiunto la stampa di questi attributi perche', non capisco come, in home.html la data viene formattata
        self.assertContains(response, self.prenotazione1.checkin.day)
        self.assertContains(response, self.prenotazione1.checkout.year)

        self.assertContains(response, self.prenotazione2.utente)
        #il template specifica solo numero e hotel
        self.assertContains(response, self.prenotazione2.camera.numero)
        self.assertContains(response, self.prenotazione2.camera.hotel.nome)
        #per ora ho aggiunto la stampa di questi attributi perche', non capisco come, in home.html la data viene formattata
        self.assertContains(response, self.prenotazione2.checkin.day)
        self.assertContains(response, self.prenotazione2.checkout.year)

if __name__ == "__main__":
    unittest.main()
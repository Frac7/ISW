#test di accettazione per la user story, visualizza la lista prenotazioni
from django.contrib.auth.models import User
from django.test import TestCase, Client
from GestioneHotel.models import *
import unittest

class TestListaPrenotazioni(TestCase):
    #task login user login, requisito
    def setUp(self):
        #Creazione albergatore (nome, cognome, email, password
        email = "user@email.com"
        password = "password"
        self.albergatore = Albergatore(nome="Pippo", cognome="Albergatore", email=email, password=password)
        self.albergatore.save()

        self.user = User(username=email)
        self.user.set_password(password)
        self.user.save()

        #Creazione indirizzi per gli hotel
        indirizzo1 = Indirizzo(via='Via Trieste', numero='14')
        indirizzo1.save()
        indirizzo2 = Indirizzo(via='Via Is Mirrionis', numero='17B')
        indirizzo2.save()

        #creazione lista di hotel che verra mostrata all'albergatore dopo il login
        self.listaHotel = []

        #creazione degli Hotel e poi aggiunta alla lista
        self.hotel1 = Hotel(nome='Grand Royal Hotel', descrizione='Hotel piu\' bello di Casteddu', citta='Cagliari', indirizzo = indirizzo1, proprietario=self.albergatore)
        self.hotel1.save()
        self.listaHotel.append(self.hotel1)
        self.hotel2 = Hotel(nome='Gold Hotel', descrizione='L\'Hotel piu\' adatto per la vostra permanenza e riposo.', citta='Cagliari',indirizzo=indirizzo2, proprietario=self.albergatore)
        self.hotel2.save()
        self.listaHotel.append(self.hotel2)

    #Una volta ch'e' stato effettuato il login, l'untente tramite il menu accede alla lista degli hotel che li appartengono
    #          e controlla se ci sono presenti tutti

    def testListaHotelPosseduti(self):
        self.assertEqual(len(Hotel.objects.all()), 2)
        self.assertEqual(len(Hotel.objects.filter(proprietario=self.albergatore)), 2)
        self.assertEqual(self.listaHotel[0], self.hotel1, "Hotel 1 non e' presente nella lista")
        self.assertEqual(self.listaHotel[1], self.hotel2, "Hotel 2 non e' presente nella lista")

    def testViewListaHotelPosseduti(self):
        # Una volta fatto il login deve essere visualizzata la home
        self.client.post("/Login/",
                         {"email": self.albergatore.email, "password": self.albergatore.password},
                         follow=True)
        # Da qui si passa alla lista hotel
        response = self.client.get("/AggiungiHotel/" + str(self.albergatore.id) + "/", follow=True)

        # Si controlla che la risposta contenga i dati degli hotel posseduti dall'albergatore loggato
        self.assertContains(response, self.hotel1.nome)
        self.assertContains(response, self.hotel2.nome)

if __name__ == "__main__":
    unittest.main()

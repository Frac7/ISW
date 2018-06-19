#test di accettazione per la user story, visualizza la lista prenotazioni
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

        #assert autorizzaAccesso(albergatore.getEmail(), albergatore.getPassword())

    #Una volta ch'e' stato effettuato il login, l'untente tramite il menu accede alla lista degli hotel che li appartengono
    #          e controlla se ci sono presenti tutti

    def testListaHotelPosseduti(self):
        self.assertEqual(len(Hotel.objects.all()), 2)
        self.assertEqual(self.listaHotel[0], self.hotel1, "Hotel 1 non e' presente nella lista")
        self.assertEqual(self.listaHotel[1], self.hotel2, "Hotel 2 non e' presente nella lista")

    def testViewListaHotelPosseduti(self):
        # Per visualizzare la lista camere e' necessario loggarsi, si manda una richiesta POST con i dati
        response = self.client.post("/Login.html/", {"email": self.albergatore.email, "password": self.albergatore.password})
        self.assertTrue(response)
        response = self.client.get("/AggiungiHotel/" + self.albergatore.id.__str__() + "/", follow=True)

        # Si controlla che la risposta contenga i dati degli hotel posseduti dall'albergatore loggato
        self.assertContains(response, self.hotel1.nome)
        # NEL TEST, FAIL ALLA RIGA SUCCESSIVA A QUESTA --------------------------------------------------------------
        self.assertContains(response, self.hotel1.descrizione)
        self.assertContains(response, self.hotel1.citta)
        for indirizzo in self.hotel1.indirizzo:
            self.assertContains(response, indirizzo.via)
            self.assertContains(response, indirizzo.numero)
        for albergatore in self.hotel1.proprietario:
            self.assertContains(response, albergatore.nome)
            self.assertContains(response, albergatore.cognome)
            self.assertContains(response, albergatore.email)
            self.assertContains(response, albergatore.password)

        self.assertContains(response, self.hotel2.nome)
        self.assertContains(response, self.hotel2.descrizione)
        self.assertContains(response, self.hotel2.citta)
        for indirizzo in self.hotel2.indirizzo:
            self.assertContains(response, indirizzo.via)
            self.assertContains(response, indirizzo.numero)
        for albergatore in self.hotel2.proprietario:
            self.assertContains(response, albergatore.nome)
            self.assertContains(response, albergatore.cognome)
            self.assertContains(response, albergatore.email)
            self.assertContains(response, albergatore.password)


if __name__ == "__main__":
    unittest.main()
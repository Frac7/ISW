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
        albergatore = Albergatore(nome="Pippo", cognome="Albergatore", email=email, password=password)
        albergatore.save()

        #Creazione indirizzi per gli hotel
        indirizzo1 = Indirizzo(via='Via Trieste', numero='14')
        indirizzo1.save()
        indirizzo2 = Indirizzo(via='Via Is Mirrionis', numero='17B')
        indirizzo2.save()

        #creazione lista di hotel che verra mostrata all'albergatore dopo il login
        listaHotel = []

        #creazione degli Hotel e poi aggiunta alla lista
        hotel1 = Hotel(nome='Grand Royal Hotel', descrizione='Hotel piu\' bello di Casteddu', citta='Cagliari', indirizzo = indirizzo1, proprietario=albergatore)
        hotel1.save()
        listaHotel.append(hotel1)
        hotel2 = Hotel(nome='Gold Hotel', descrizione='L\'Hotel piu\' adatto per la vostra permanenza e riposo.', citta='Cagliari',indirizzo=indirizzo2, proprietario=albergatore)
        hotel2.save()
        listaHotel.append(hotel2)

        #controllo se nella lista sono presenti gli hotel sopra dichiarati
        assert listaHotel[0] == hotel1
        assert listaHotel[1] == hotel2

        #assert autorizzaAccesso(albergatore.getEmail(), albergatore.getPassword())

    #Una volta ch'e' stato effettuato il login, l'untente tramite il menu accede alla lista degli hotel che li appartengono
    #          e controlla se ci sono presenti tutti

    def testListaHotelPosseduti(self):
        self.assertEqual(len(Hotel.objects.all()), 2)


if __name__ == "__main__":
    unittest.main()
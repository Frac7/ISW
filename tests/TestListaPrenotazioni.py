from django.test import TestCase
import unittest
from GestioneHotel.models import *

#test di accettazione per la user story, visualizza la lista prenotazioni
class TestListaPrenotazioni(TestCase):
    #task login user login, requisito
    def testLogin(self):
        #Creazione albergatore (nome, cognome, email, password
        email = "user@name"
        password = "password"
        albergatore = Albergatore(nome="Pippo", cognome="Albergatore", email=email, password=password)
        #self.assertEqual(albergatore.nome,"Pippo")
        #Controlla che i dati inseriti siano validi per il login
        #assert autorizzaAccesso(albergatore.getEmail(), albergatore.getPassword())

    #Una volta loggato, l'utente accede dal menu alla lista delle prenotazioni che li mostra la lista delle prenotazioni
    #                   con i dati relativi ad ogni prenotazione
if __name__ == "__main__":
    unittest.main()
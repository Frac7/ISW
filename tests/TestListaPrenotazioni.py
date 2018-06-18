#test di accettazione per la user story, visualizza la lista prenotazioni
from django.test import TestCase
from datetime import date
from GestioneHotel.models import *
import unittest

class TestListaPrenotazioni(TestCase):
    #task login user login, requisito
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "user@email.com"
        password = "password"
        albergatore = Albergatore(nome="Pippo", cognome="Albergatore", email=email, password=password)
        albergatore.save()

        # Creazione indirizzi per gli hotel
        indirizzo1 = Indirizzo(via='Via Trieste', numero='14')
        indirizzo1.save()

        # creazione degli Hotel e poi aggiunta alla lista
        hotel1 = Hotel(nome='Gold Hotel', descrizione='L\'Hotel piu\' adatto per la vostra permanenza e riposo.', citta='Cagliari', indirizzo=indirizzo1, proprietario=albergatore)
        hotel1.save()

        #Creazione servizi per i servizi disponibili
        servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        servizio.save()

        #Creazione delle camere che verranno mostrate nella lista delle prenotazioni in corso (che verranno mostrate nella lista all'albergatore)
        camera1 = Camera(numero=1, postiLetto=4, hotel=hotel1)
        camera1.save()
        camera2 = Camera(numero=2, postiLetto=3, hotel=hotel1)
        camera2.save()

        #Lego i servizi alle camere
        servizioTv = ServiziDisponibili(camera=camera1, servizio=servizio)
        servizioTv.save()
        servizioTv = ServiziDisponibili(camera=camera1, servizio=servizio)
        servizioTv.save()

        #Creazione lista delle prenotazioni che saranno visibili all'Albergatore in prima pagina, come si logga
        listaPrenotazioni = []


        #Creazione e aggiunta delle prenotazioni alla lista che verra mostrata all'Albergatore
        prenotazione1 = Prenotazione(utente='utenteNonRegistrato1@gmail.it', camera=camera1, checkin=date(2012, 3, 15),
                                     checkout=date(2011, 8, 30))
        prenotazione1.save()
        listaPrenotazioni.append(prenotazione1)
        prenotazione2 = Prenotazione(utente='ntenteNonRegistrato2@gmail.it', camera=camera2, checkin=date(2012, 3, 8),
                                     checkout=date(2011, 8, 30))
        prenotazione2.save()
        listaPrenotazioni.append(prenotazione2)

        #assert autorizzaAccesso(albergatore.getEmail(), albergatore.getPassword())

    #Una volta loggato, l'utente accede dal menu alla lista delle prenotazioni che li mostra la lista delle prenotazioni
    #                   con i dati relativi ad ogni prenotazione


    def testListaPrenotazioni(self):
        self.assertEqual(len(Prenotazione.objects.all()), 2)

if __name__ == "__main__":
    unittest.main()
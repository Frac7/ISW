#Test unitario classe Hotel
#I test falliscono per via del login richiesto; non e' possibile fare il login perche' nel server ancora non esiste url Login
from GestioneHotel.models import *
from django.test import TestCase, Client
import unittest

class TestHotel(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "username@dominio"
        password = "unaPassword"
        self.albergatore = Albergatore(nome="un", cognome="Albergatore", email=email, password=password)
        self.albergatore.save()
        # Creazione singolo servizio: nome e descrizione
        servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        servizio.save()
        # Indirizzo hotel
        indirizzo = Indirizzo(via="Via Ospedale", numero="72")
        indirizzo.save()
        # Hotel in cui e' presente la camera
        self.hotel = Hotel(nome="unHotel", descrizione="unHotelACagliari", citta="Cagliari", indirizzo=indirizzo, proprietario=self.albergatore)
        self.hotel.save()
        # Crea una camera con dei dati
        # Camera(numero, posti letto, servizi, hotel)
        self.camera = Camera(numero=1, postiLetto=4, hotel=self.hotel)
        self.camera.save()
        #Servizi a disposizione per la camera
        servizi = ServiziDisponibili(camera=self.camera, servizio=servizio)
        servizi.save()
        #Creazione client per test richiesta/risposta
        self.client = Client()

    def testModelsListaCamere(self):
        #Test models (test con gli oggetti del DB)
        camera = Camera.objects.all().get(id=self.camera.id)
        self.assertEqual(camera.hotel, self.hotel, "Camera non aggiunta")
        self.assertEqual(len(Camera.objects.all()), 1, "La lunghezza della lista camera e\' diversa da 1")
        self.assertEqual(len(camera.hotel.listaCamere()), 1, "La lunghezza della lista camera e\' diversa da 1")
        self.assertEqual(Camera.objects.all().get(id=self.camera.id), Camera.objects.filter(hotel=self.hotel).get(id=self.camera.id))

    def testViewsListaCamere(self):
        #Per visualizzare la lista camere e' necessario loggarsi, si manda una richiesta POST con i dati
        response = self.client.post("/Login/", {"email": self.albergatore.email, "password": self.albergatore.password})
        self.assertTrue(response)
        #Visualizzazione pagina lista camere di un certo hotel
        response = self.client.get("/InfoHotelAggiungiCamera/" + self.hotel.id.__str__() +"/", follow=True)
        #Si controlla che la risposta contenga i dati delle camere
        self.assertContains(response, self.camera.numero)
        self.assertContains(response, self.camera.postiLetto)
        for servizi in self.camera.listaServizi():
            for servizio in servizi:
                self.assertContains(response, servizio.nome)
                self.assertContains(response, servizio.descrizioneServizio)
        self.assertNotContains(response, "WI-FI")

    def testViewsUtenteNonLoggato(self):
        response = self.client.get("/InfoHotelAggiungiCamera/" + self.hotel.id.__str__() +"/")
        self.assertEquals(response.status_code, 302)
        #Redirection (login e poi info hotel)
        self.assertEquals(response.url, "/Login?next=/InfoHotelAggiungiCamera/" + self.hotel.id.__str__() +"/")

    def testModelsHotel(self):
        self.assertEqual(len(Hotel.objects.all()), 1, "La lunghezza della lista hotel e\' diversa da 1")
        unAltroHotel = Hotel('unAltroHotel','unHotelDiversoDalPrecedente',"Roma",self.hotel.indirizzo,self.hotel.proprietario)
        self.assertNotEqual(self.hotel, unAltroHotel)
        self.assertNotEqual(self.camera.hotel, unAltroHotel)

    def testViewsHotel(self):
        response = self.client.post("/Login/", {"email": self.albergatore.email, "password": self.albergatore.password})
        self.assertTrue(response)
        response = self.client.get("/InfoHotelAggiungiCamera/" + self.hotel.id.__str__() + "/", follow=True)
        #Si controlla che la risposta contenga i dati dell'hotel
        self.assertContains(response, self.hotel.nome)
        self.assertContains(response, self.hotel.descrizione)
        self.assertContains(response, self.hotel.indirizzo.via)
        self.assertContains(response, self.hotel.indirizzo.numero)

    def testViewsAggiungiCamera(self):
        response = self.client.post("/Login/", {"email": self.albergatore.email, "password": self.albergatore.password})
        self.assertTrue(response)
        #Invio form
        response = self.client.post("/InfoHotelAggiungiCamera/" + self.hotel.id.__str__() + "/",
                                    {"numero": "101", "postiLetto": "1", "serivizio1": True, "serivizio2": False, "serivizio3": False }, follow=True)
        # Si controlla che la risposta contenga i dati della camera inserita
        self.assertContains(response, "101")
        self.assertContains(response, "1")

if __name__ == "__main__":
    unittest.main()



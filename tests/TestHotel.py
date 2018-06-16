#Test unitario classe Hotel
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
        self.assertEqual(Camera.objects.all().get(id=self.camera.id), Camera.objects.filter(hotel=self.hotel).get(id=self.camera.id))

    def testViewsListaCamere(self):
        #Per visualizzare la lista camere e' necessario loggarsi, si manda una richiesta POSR con i dati
        response = self.client.post("/Login.html/", {"email": self.albergatore.email, "password": self.albergatore.password})
        self.assertTrue(response)
        #Visualizzazione pagina lista camere di un certo hotel
        response = self.client.get("/InfoHotelAggiungiCamera.html?hotelID=" + self.hotel.id.__str__() +"/", follow=True)
        #Si controlla che la risposta contenga i dati delle camere
        self.assertContains(response, self.camera.numero)
        self.assertContains(response, self.camera.postiLetto)
        for servizio in self.camera.servizi:
            self.assertContains(response, servizio.nome)
            self.assertContains(response, servizio.descrizione)
        self.assertNotContains(response, 2)
        self.assertNotContains(response, "WI-FI")

    def testViewsUtenteNonLoggato(self):
        response = self.client.get("/InfoHotelAggiungiCamera.html?hotelID=" + self.hotel.id.__str__() +"/")
        self.assertEquals(response.status_code, 302)
        #Redirection (login e poi info hotel)
        self.assertEquals(response.url, "/Login.html/?next=/InfoHotelAggiungiCamera.html/")

    def testModelsHotel(self):
        self.assertEqual(len(Hotel.objects.all()), 1, "La lunghezza della lista hotel e\' diversa da 1")
        unAltroHotel = Hotel('unAltroHotel','unHotelDiversoDalPrecedente',"Roma",self.hotel.indirizzo,self.hotel.proprietario)
        self.assertNotEqual(self.hotel, unAltroHotel)
        self.assertNotEqual(self.camera.hotel, unAltroHotel)

    def testViewsHotel(self):
        response = self.client.post("/Login.html/", {"email": self.albergatore.email, "password": self.albergatore.password})
        self.assertTrue(response)
        response = self.client.get("/InfoHotelAggiungiCamera.html?hotelID=" + self.hotel.id.__str__() + "/", follow=True)
        #Si controlla che la risposta contenga i dati dell'hotel
        self.assertContains(response, self.hotel.nome)
        self.assertContains(response, self.hotel.descrizione)
        self.assertContains(response, self.hotel.indirizzo.via)
        self.assertContains(response, self.hotel.indirizzo.numero)

if __name__ == "__main__":
    unittest.main()



 # -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth import authenticate
from django.test import TestCase, Client
from GestioneHotel.models import *
import unittest

# Test Unitari.

class ModelTest(TestCase):
    # Creazione di Un Hotel
    def setUp(self):
        albergatore1 = Albergatore(nome="Pino", cognome='Pipetta', email='pinopipetta@outlook.com', password='ninnito42')
        albergatore1.save()
        albergatore2 = Albergatore(nome="Pippo", cognome='Pluto', email='pippopluto@outlook.com', password='cosimo83')
        albergatore2.save()
        self.hotel1=Hotel(nome="Hilton", descrizione="Il Migliore!", email="hilton@hilton.com",password="123")
        self.hotel1.save()
        self.hotel2=Hotel(nome="Hilton", descrizione="Il Migliore!", email="hilton@hilton.com",password="123")
        self.hotel2.save()
    # Conteggio Hotels
    def testCountHotels(self):
        self.assertEqual(len(Hotel.objects.all()),2)

    def testCountAlbergatores(self):
        self.assertEqual(len(Albergatore.objects.all()), 2)


if __name__ == '__main__':
    unittest.main()


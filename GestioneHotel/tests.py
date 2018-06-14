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
        self.hotel1=Hotel(nome="Hilton", descrizione="Il Migliore!", email="hilton@hilton.com",password="123")
        self.hotel1.save()
        self.hotel2=Hotel(nome="Hilton", descrizione="Il Migliore!", email="hilton@hilton.com",password="123")
        self.hotel2.save()
    # Conteggio Hotels
    def testCountHotels(self):
        self.assertEqual(len(Hotel.objects.all()),2)


if __name__ == '__main__':
    unittest.main()


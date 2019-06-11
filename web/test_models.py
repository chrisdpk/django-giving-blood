from django.test import TestCase
from .models import Donation, DonationPlace
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class ProfileModelTest(TestCase):

    def testGetDateInAllowedIntervalFalse(self):
        u = User.objects.create()
        Donation.objects.create(user=u, donationdate=datetime.now())

        self.assertFalse(u.profile.date_in_allowed_interval(datetime.now()))

    def testGetDateInAllowedIntervalFalse2(self):
        u = User.objects.create()
        Donation.objects.create(user=u, donationdate=datetime.now())
        c_date = datetime.now() + timedelta(days=1)
        self.assertFalse(u.profile.date_in_allowed_interval(c_date))

    def testGetDateInAllowedIntervalTrue(self):
        u = User.objects.create()
        Donation.objects.create(user=u, donationdate=datetime.now())
        c_date = datetime.now() + timedelta(days=58)
        self.assertTrue(u.profile.date_in_allowed_interval(c_date))

    def testGetNextDonationDate(self):
        pass


class DonationPlaceModelTest(TestCase):

    def testGetAddress(self):
        u = User.objects.create()
        d = DonationPlace.objects.create(name="Place Name", street="Ul. Przykład", house="3a",
                                         address_supplement="M. 4c", postal_code="10-234", city="Kraków", country="PL",
                                         contributor=u)
        self.assertSequenceEqual(d.get_address(), "Ul. Przykład 3a, M. 4c, 10-234 Kraków, POLAND")

    def testGetStr(self):
        u = User.objects.create()
        d = DonationPlace.objects.create(name="Place Name", street="Ul. Przykład", house="3a",
                                         address_supplement="M. 4c", postal_code="10-234", city="Kraków", country="PL",
                                         contributor=u)
        self.assertSequenceEqual(str(d), "Place Name, Ul. Przykład 3a, M. 4c, 10-234 Kraków, POLAND")

    def testGetUrl(self):
        u = User.objects.create()
        d = DonationPlace.objects.create(name="Place Name", street="Ul. Przykład", house="3a",
                                         address_supplement="M. 4c", postal_code="10-234", city="Kraków", country="PL",
                                         contributor=u)
        self.assertSequenceEqual(d.get_maps_url(), "https://www.google.com/maps/?q=Ul.%20Przyk%C5%82ad%203a,%20M.%204c,%2010-234%20Krak%C3%B3w,%20POLAND")

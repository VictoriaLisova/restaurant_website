from django.test import TestCase
from django.utils import timezone
from reservation.models import Reservation


class TestReservation(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.reservation1 = Reservation.objects.create(name='John Doe', email='john@example.com', phone=123456789,
                                                       number_of_persons=4, date=timezone.now().date(),
                                                       time=timezone.now().time())
        cls.reservation2 = Reservation.objects.create(name='Jane Smith', email='jane@example.com', phone=987654321,
                                                       number_of_persons=2, date=timezone.now().date(),
                                                       time=timezone.now().time())

    def test_reservation_name(self):
        self.assertEquals(self.reservation1.__str__(), 'John Doe')
        self.assertEquals(self.reservation2.__str__(), 'Jane Smith')

    def test_reservation_count(self):
        reservations_count = Reservation.objects.count()
        self.assertEquals(reservations_count, 2)

    def test_reservation_email(self):
        reservation = Reservation.objects.get(name='John Doe')
        self.assertEquals(reservation.email, 'john@example.com')

    def test_reservation_phone(self):
        reservation = Reservation.objects.get(name='Jane Smith')
        self.assertEquals(reservation.phone, 987654321)

    def test_reservation_date(self):
        reservation = Reservation.objects.get(name='John Doe')
        self.assertEquals(reservation.date, timezone.now().date())


from django.test import TestCase, Client
from reservation.models import Reservation
from reservation.forms import ReserveTableForm
import datetime


class TestReservationView(TestCase):
    def test_reserve_table_GET(self):
        response = self.client.get('/reserve/')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Reservation/reservation.html')
        self.assertIsInstance(response.context['form'], ReserveTableForm)

    def test_reserve_table_POST_invalid_data(self):
        invalid_data = {
            'name': 'Test User',
            'email': 'invalidemail',
            'phone': '123456789',
            'number_of_persons': 1,
            'date': '2024',
            'time': '18:00',
        }
        response = self.client.post('/reserve/', data=invalid_data)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Reservation/reservation.html')

        form = response.context['form']

        self.assertTrue('email' in form.errors)
        self.assertTrue('date' in form.errors)

    def test_reserve_table_POST_valid_data(self):
        valid_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '123456789',
            'number_of_persons': 4,
            'date': datetime.date(2024, 5, 16),  # Future date
            'time': '18:00',
        }
        response = self.client.post('/reserve/', data=valid_data)
        self.assertEquals(response.status_code, 200)

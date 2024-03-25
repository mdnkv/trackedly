from django.test import TestCase
from django.contrib.auth import get_user_model

from datetime import date, time

from entries.forms import EntryForm

from faker import Faker

User = get_user_model()
faker = Faker()


class EntryFormTest(TestCase):

    def test_validate_finish_date_after_start_date(self):
        """
        Validate that the finish date should be after the start date or same day
        """
        user = User.objects.create_user(email=faker.email(), password='secret1234')
        start_date = date(year=2024, month=3, day=25)
        finish_date = date(year=2024, month=3, day=24)
        start_time = time(10, 00, 00)
        finish_time = time(10, 30, 00)
        data = {
            'description': faker.paragraph(nb_sentences=1),
            'start_date': start_date,
            'finish_date': finish_date,
            'start_time': start_time,
            'finish_time': finish_time,
            'project': ''
        }
        form = EntryForm(user=user, data=data)
        self.assertFalse(form.is_valid())

    def test_validate_finish_time_after_start_time(self):
        """
        Validate that the finish time should be after the start time
        """
        user = User.objects.create_user(email=faker.email(), password='secret1234')
        start_date = date(year=2024, month=3, day=25)
        finish_date = date(year=2024, month=3, day=25)
        start_time = time(10, 00, 00)
        finish_time = time(9, 30, 00)
        data = {
            'description': faker.paragraph(nb_sentences=1),
            'start_date': start_date,
            'finish_date': finish_date,
            'start_time': start_time,
            'finish_time': finish_time,
            'project': ''
        }
        form = EntryForm(user=user, data=data)
        self.assertFalse(form.is_valid())

    def test_entry_form_is_valid(self):
        """
        Validate that EntryForm is valid
        """
        user = User.objects.create_user(email=faker.email(), password='secret1234')
        start_date = date(year=2024, month=3, day=25)
        finish_date = date(year=2024, month=3, day=25)
        start_time = time(10, 00, 00)
        finish_time = time(10, 30, 00)
        data = {
            'description': faker.paragraph(nb_sentences=1),
            'start_date': start_date,
            'finish_date': finish_date,
            'start_time': start_time,
            'finish_time': finish_time,
            'project': ''
        }
        form = EntryForm(user=user, data=data)
        self.assertTrue(form.is_valid())

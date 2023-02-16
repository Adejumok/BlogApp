from django.test import TestCase

from blog.models import Writer


class WriterModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Writer.objects.create(first_name='Wale', last_name='Samuel', email='wale@gmail.com', id=1)

    def test_first_name_label(self):
        writer = Writer.objects.get(id=1)
        field_label = writer._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        writer = Writer.objects.get(id=1)
        field_label = writer._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_email_label(self):
        writer = Writer.objects.get(id=1)
        field_label = writer._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_last_name_max_length(self):
        writer = Writer.objects.get(id=1)
        max_length = writer._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 255)

    def test_object_name_is_first_name_comma_last_name(self):
        writer = Writer.objects.get(id=1)
        expected_object_name = f'{writer.first_name} {writer.last_name}'
        self.assertEqual(str(writer), expected_object_name)

    def test_get_absolute_url(self):
        writer = Writer.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(writer.get_absolute_url(), '/blog/writer/1')

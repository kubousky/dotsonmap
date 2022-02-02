from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email='test@kubousky.com', password='test'):
    """" Create a sample user """
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):

    def test_create_user_with_email_succesfull(self):
        """Test creating a new user with an email is succesful"""
        email = "test@kubousky.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = "test@KUBOUSKY.com"
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """If the error is not raised the test will fail"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test123')

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            "test@kubousky.com",
            "testpass123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Temple'
        )

        self.assertEqual(str(tag), tag.name)

    def test_dot_str(self): # !!! lo vamos a cambiar por un imagen de su Tag, cada 'dot' ser un circulo con rio o montaña etc
        """test the recipe string representation"""
        dot = models.Dot.objects.create(
            user=sample_user(),
            name='Bromo',
            description='Es un Volcan en Indonesia',
            lon='13.9923',
            lat='34.7823',
            rating=4.5,
        )

        self.assertEqual(str(dot), dot.name)
from django.test import TestCase
from django.contrib.auth import get_user_model

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
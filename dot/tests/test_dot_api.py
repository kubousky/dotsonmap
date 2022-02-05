from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Dot, Tag

from dot.serializers import DotSerializer, DotDetailSerializer


DOT_URL = reverse('dot:dot-list')


def detail_url(dot_id):
    """Return dot detail URL"""
    return reverse('dot:dot-detail', args=[dot_id])


def sample_tag(user, name='Waterfall'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_dot(user, **params):
    """Create and returns a sample dot"""
    defaults = {
        'name': 'Thousand Waterfalls',
        'lon': '12.98832',
        'lat': '45.87321'
    }
    defaults.update(params)

    return Dot.objects.create(user=user, **defaults)

class PublicDotApiTests(TestCase):
    """Test unauthenticated dot API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(DOT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateDotApiTests(TestCase):
    """Test unauthenticated dot API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@kubousky.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_dots(self):
        """"Test retrieving a list of dots"""

        sample_dot(user=self.user)
        sample_dot(user=self.user)

        res = self.client.get(DOT_URL)

        dots = Dot.objects.all().order_by('id')
        serializer = DotSerializer(dots, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_dots_limited_to_user(self): ## probablemente hay que cambiarlo
        """Test retrieving dots for user"""
        user2 = get_user_model().objects.create_user(
            'other@kubousky.com',
            'password123'
        )
        sample_dot(user=user2)
        sample_dot(user=self.user)

        res = self.client.get(DOT_URL)

        dots = Dot.objects.filter(user=self.user)
        serializer = DotSerializer(dots, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_dot_detail(self):
        """Test viewing a dot detail"""
        dot = sample_dot(user=self.user)
        dot.tags.add(sample_tag(user=self.user))

        url = detail_url(dot.id)
        res = self.client.get(url)

        serializer = DotDetailSerializer(dot)
        self.assertEqual(res.data, serializer.data)



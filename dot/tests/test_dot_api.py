import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import DotPrivate, TagPrivate

from dot.serializers import DotPrivateSerializer, DotPrivateDetailSerializer


DOT_URL = reverse('dot:dot-list')


def image_upload_url(dot_id):
    """Return URL for dot image upload"""
    return reverse('dot:dot-upload-image', args=[dot_id])

def detail_url(dot_id):
    """Return dot detail URL"""
    return reverse('dot:dot-detail', args=[dot_id])


def sample_tag(user, name='Waterfall'):
    """Create and return a sample tag"""
    return TagPrivate.objects.create(user=user, name=name)


def sample_dot(user, **params):
    """Create and returns a sample dot"""
    defaults = {
        'name': 'Thousand Waterfalls',
        'lon': '12.98832',
        'lat': '45.87321',
        'rating': '4.5'
    }
    defaults.update(params)

    return DotPrivate.objects.create(user=user, **defaults)

class PublicDotPrivateApiTests(TestCase):
    """Test unauthenticated dot API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(DOT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateDotPrivateApiTests(TestCase):
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

        dots = DotPrivate.objects.all().order_by('id')
        serializer = DotPrivateSerializer(dots, many=True)

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

        dots = DotPrivate.objects.filter(user=self.user)
        serializer = DotPrivateSerializer(dots, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_dot_detail(self):
        """Test viewing a dot detail"""
        dot = sample_dot(user=self.user)
        dot.tags.add(sample_tag(user=self.user))

        url = detail_url(dot.id)
        res = self.client.get(url)

        serializer = DotPrivateDetailSerializer(dot)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_dot(self):
        """Test creating dot"""
        payload = {
            'name': 'Peña Cortada',
            'lat': '18.35678',
            'lon': '67.76333',
            'rating': 5.0
        }
        res = self.client.post(DOT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        dot = DotPrivate.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(dot, key))

    def test_create_dot_with_tags(self):
        """Test creating a dot with tags"""
        tag1 = sample_tag(user=self.user, name='Waterfall')
        tag2 = sample_tag(user=self.user, name='Mountain')
        payload = {
            'name': 'Peña Cortada',
            'lat': '18.35678',
            'lon': '67.76333',
            'rating': '5.0',
            'tags': [tag1.id, tag2.id]
        }
        res = self.client.post(DOT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        dot = DotPrivate.objects.get(id=res.data['id'])
        tags = dot.tags.all()
        self.assertEqual(tags.count(),2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags) 

class DotPrivateImageUploadTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@kubousky.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        self.dot = sample_dot(user=self.user)

    def tearDown(self):
        self.dot.image.delete()

    def test_upload_image_to_dot(self):
        """Test uploading an image to dot"""
        url = image_upload_url(self.dot.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')
        
        self.dot.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.dot.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.dot.id)
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_dot_by_tags(self):
        """Test returning dots with specific tags"""
        dot1 = sample_dot(user=self.user, name='Castillo de Serra')
        dot2 = sample_dot(user=self.user, name='Cala de Bingo')
        tag1 = sample_tag(user=self.user, name='Castle')
        tag2 = sample_tag(user=self.user, name='Beach')
        dot1.tags.add(tag1)
        dot2.tags.add(tag2)
        dot3 = sample_dot(user=self.user, name='Museo fallera')

        res = self.client.get(
            DOT_URL,
            {'tags': f'{tag1.id},{tag2.id}'}
        )

        serializer1 = DotPrivateSerializer(dot1)
        serializer2 = DotPrivateSerializer(dot2)
        serializer3 = DotPrivateSerializer(dot3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)





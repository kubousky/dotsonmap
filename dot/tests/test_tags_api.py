from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Dot

from dot.serializers import TagSerializer


TAGS_URL = reverse('dot:tag-list')


class PublicTagsApiTests():
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    """TEST the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@kubousky.com'
            'password123'
        )         
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name='Temple')
        Tag.objects.create(user=self.user, name='Mountain')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@kubousky.com',
            'testpass'
        )
        Tag.objects.create(user=user2, name='Waterfall')
        tag = Tag.objects.create(user=self.user, name='River')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_succesful(self):
        """Test creating a new tag"""
        payload = {'name' : 'Test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retrieve_tags_assigned_to_dot(self):
        """Test filtering tags by those assigned to dots"""

        tag1 = Tag.objects.create(user=self.user, name='Castle')
        tag2 = Tag.objects.create(user=self.user, name='Beach')
        dot = Dot.objects.create(
            name= 'Peña Cortada',
            lat= '18.35678',
            lon= '67.76333',
            rating= '5.0',
            user=self.user
        )
        dot.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only':1})

        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2, res.data)

    def test_retrieve_tags_assigned_unique(self): # in a future Dot will have assigned only 1 tag
        """Test filtering tags by assigned returns unique item"""

        tag = Tag.objects.create(user=self.user, name='Lake')
        Tag.objects.create(user=self.user, name="Castle")
        dot1 = Dot.objects.create(
            name= 'Albufera',
            lat= '18.35678',
            lon= '67.76333',
            rating= '5.0',
            user=self.user
        )
        dot1.tags.add(tag)
        dot2 = Dot.objects.create(
            name= 'Xativa Castle',
            lat= '18.35678',
            lon= '67.76333',
            rating= '5.0',
            user=self.user
        )
        dot1.tags.add(tag)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
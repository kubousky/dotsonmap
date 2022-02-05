from django.test import tag
from rest_framework import serializers

from core.models import Tag, Dot


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class DotSerializer(serializers.ModelSerializer):
    """Serializer for dot objects"""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    
    class Meta:
        model = Dot
        fields = ('id', 'name', 'description', 'lat', 'lon', 'rating', 'link', 'tags')
        read_only_fields = ('id',)

class DotDetailSerializer(DotSerializer):
    """Serialize a dot detail"""
    tags = TagSerializer(many=True, read_only=True) 
from django.test import tag
from rest_framework import serializers

from core.models import TagPrivate, DotPrivate


class TagPrivateSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = TagPrivate
        fields = ('id', 'name')
        read_only_fields = ('id',)


class DotPrivateSerializer(serializers.ModelSerializer):
    """Serializer for dot objects"""

    tag = serializers.PrimaryKeyRelatedField(
        queryset=TagPrivate.objects.all() # if .filter(user=request.user.id) -> request is not defined error
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        self.fields['tag'].queryset=TagPrivate.objects.filter(user=request.user.id)
    
    class Meta:
        model = DotPrivate
        fields = ('id', 'name', 'description', 'lat', 'lon', 'rating', 'link', 'tag')
        read_only_fields = ('id',)

class DotPrivateDetailSerializer(DotPrivateSerializer):
    """Serialize a dot detail"""
    tag = TagPrivateSerializer(read_only=True)

class DotPrivateImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to dots"""

    class Meta:
        model = DotPrivate
        fields = ('id', 'image')
        read_only_fields = ('id',)
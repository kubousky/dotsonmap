from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Dot

from dot import serializers

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self): # overwriting the current method
        """"Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer): # overwriting
        """Create a new tag by an auth user"""
        serializer.save(user=self.request.user)

class DotViewSet(viewsets.ModelViewSet):
    """Manage dot in the database"""
    serializer_class = serializers.DotSerializer
    queryset = Dot.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self): # overwriting the current method
        """"Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropiate serializer class"""
        if self.action == 'retrieve':
            return serializers.DotDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new dot"""
        serializer.save(user=self.request.user)





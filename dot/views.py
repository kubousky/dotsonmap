from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
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

        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(dot__isnull=False) # retrieve Tags that are assigned to dots
        
        return queryset.filter(user=self.request.user).order_by('-name').distinct()

    def perform_create(self, serializer): # overwriting
        """Create a new tag by an auth user"""
        serializer.save(user=self.request.user)

class DotViewSet(viewsets.ModelViewSet):
    """Manage dot in the database"""
    serializer_class = serializers.DotSerializer
    queryset = Dot.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to list of integers"""
        return [int(str_id) for str_id in qs.split(',')]


    def get_queryset(self): # overwriting the current method
        """"Return objects for the current authenticated user only"""
        tags = self.request.query_params.get('tags')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropiate serializer class"""
        if self.action == 'retrieve':
            return serializers.DotDetailSerializer
        elif self.action == 'upload_image':
            return serializers.DotImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new dot"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a dot"""
        dot = self.get_object() # object based on an id
        serializer = self.get_serializer(
            dot,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



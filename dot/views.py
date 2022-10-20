from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import TagPrivate, DotPrivate, User#, TagPublic, DotPublic

from dot import serializers

class TagPrivateViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = TagPrivate.objects.all()
    serializer_class = serializers.TagPrivateSerializer

    def get_queryset(self): # overwriting the current method
        """"Return objects for the current authenticated user only"""

        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(dot__isnull=False) # retrieve TagPrivate that are assigned to dots
        
        return queryset.filter(user=self.request.user).order_by('-name').distinct()

    def perform_create(self, serializer): # overwriting
        """Create a new tag by an auth user"""
        serializer.save(user=self.request.user)

class DotPrivateViewSet(viewsets.ModelViewSet):
    """Manage dot in the database"""
    serializer_class = serializers.DotPrivateSerializer
    queryset = DotPrivate.objects.all()
    # authentication_classes = (TokenAuthentication,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    # serializer = serializers.DotPrivateSerializer()
    # print(repr(serializer))

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self): # overwriting the current method
        """"Return objects for the current authenticated user only"""
        tags = self.request.query_params.get('tag') # <QueryDict: {'tag': ['2']}>
        queryset = self.queryset
        if tags: 
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tag__id__in=tag_ids) # /api/dot/dots/?tag=2
        return queryset.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(request=self.request)
        return context

    def get_serializer_class(self):
        """Return appropiate serializer class"""
        if self.action == 'retrieve':
            return serializers.DotPrivateDetailSerializer
        elif self.action == 'upload_image':
            return serializers.DotPrivateImageSerializer

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



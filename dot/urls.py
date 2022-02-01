from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dot import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'dot'

urlpatterns = [
    path('', include(router.urls))
]
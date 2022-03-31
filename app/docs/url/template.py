from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views import TemplateViewset

app_name = 'card'

router = DefaultRouter()
router.register('', TemplateViewset)


urlpatterns = [
    path('', include(router.urls)),
]
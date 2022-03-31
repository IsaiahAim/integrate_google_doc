from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views import MemoViewset

app_name = 'card'

router = DefaultRouter()
router.register('', MemoViewset)


urlpatterns = [
    path('', include(router.urls)),
]
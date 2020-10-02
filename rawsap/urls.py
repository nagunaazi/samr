from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


router = DefaultRouter()
router.register('ZVT_PORTAL_CIRViewSet',ZVT_PORTAL_CIRViewSet,basename='ZVT_PORTAL_CIRViewSet')

urlpatterns = [
]
urlpatterns += router.urls
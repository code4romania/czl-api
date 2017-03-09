from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'institutions', views.InstitutionViewSet)
router.register(r'publications', views.PublicationViewSet)
router.register(r'documents', views.DocumentViewSet)

urlpatterns = router.urls

from rest_framework import viewsets, mixins, permissions
from .models import Institution, Publication, Document
from .serializers import (
    InstitutionSerializer, PublicationSerializer, DocumentSerializer,
)


# everything is read-only
class InstitutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


# except for publications, which are read/create-only
class PublicationViewSet(mixins.CreateModelMixin,
                         viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

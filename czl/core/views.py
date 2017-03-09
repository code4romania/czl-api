from rest_framework import viewsets, mixins, permissions
from .models import Institution, Publication, Document
from .serializers import (
    InstitutionSerializer, PublicationSerializer, DocumentSerializer,
)


# institutions are read-only
class InstitutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


# while the rest is read/create-only, and requires auth
class _WritableViewSet(mixins.CreateModelMixin,
                       viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class PublicationViewSet(_WritableViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


class DocumentViewSet(_WritableViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

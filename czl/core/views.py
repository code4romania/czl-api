from rest_framework import viewsets, mixins, permissions
from rest_framework import pagination
from .models import Institution, Publication, Document
from .serializers import (
    InstitutionSerializer, PublicationSerializer, DocumentSerializer,
)


# institutions are read-only
class InstitutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    pagination_class = None


# while the rest is read/create-only, and requires auth
class _WritableViewSet(mixins.CreateModelMixin,
                       viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class _PublicationPagination(pagination.CursorPagination):
    ordering = '-date'


class PublicationViewSet(_WritableViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    pagination_class = _PublicationPagination


class DocumentViewSet(_WritableViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    pagination_class = pagination.LimitOffsetPagination

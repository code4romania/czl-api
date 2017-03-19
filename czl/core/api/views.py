from rest_framework import viewsets, mixins, permissions
from rest_framework import pagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Institution, Publication, Document
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


# TODO: this is the correct, predictable, non-repeating pagination,
# .. to be implemented some time in the future
class _PublicationPagination(pagination.CursorPagination):
    ordering = '-created_at'


class PublicationViewSet(_WritableViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filter_fields = (
        'institution',
        'type',
    )
    ordering_fields = (
        'date',
        '_created_at',
    )
    ordering = '-date'


class DocumentViewSet(_WritableViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    pagination_class = pagination.PageNumberPagination

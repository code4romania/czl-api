from rest_framework import serializers, fields
from drf_enum_field.serializers import EnumFieldSerializerMixin
from .models import Institution, Publication, Document


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution


class PublicationSerializer(EnumFieldSerializerMixin,
                            serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Publication


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document

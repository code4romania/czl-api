from rest_framework import serializers
from drf_enum_field.serializers import EnumFieldSerializerMixin
from .models import Organization, Publication, Document


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization


class PublicationSerializer(EnumFieldSerializerMixin,
                            serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Publication


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document

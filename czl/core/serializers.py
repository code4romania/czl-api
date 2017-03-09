from rest_framework import serializers, fields
from drf_enum_field.serializers import EnumFieldSerializerMixin
from .models import Institution, Publication, Document


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document


class NestedDocumentSerializer(DocumentSerializer):
    class Meta(DocumentSerializer.Meta):
        exclude = ('publication', 'id')


class PublicationSerializer(EnumFieldSerializerMixin,
                            serializers.ModelSerializer):
    documents = NestedDocumentSerializer(many=True, required=False)

    class Meta:
        model = Publication
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        docs_data = validated_data.pop('documents', [])
        publication = super().create(validated_data)

        for doc_data in docs_data:
            Document.objects.create(publication=publication, **doc_data)

        return publication

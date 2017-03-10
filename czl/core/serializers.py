from rest_framework import serializers, fields
from drf_enum_field.serializers import EnumFieldSerializerMixin
from .models import Institution, Publication, Document


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ('submitted_by', )


class NestedDocumentSerializer(DocumentSerializer):
    class Meta(DocumentSerializer.Meta):
        exclude = ('publication', 'id', 'submitted_by')


class PublicationSerializer(EnumFieldSerializerMixin,
                            serializers.ModelSerializer):
    documents = NestedDocumentSerializer(many=True, required=False)

    class Meta:
        model = Publication
        extra_kwargs = {'id': {'read_only': True}}
        exclude = ('submitted_by', )

    def create(self, validated_data):
        docs_data = validated_data.pop('documents', [])
        user = self.context['request'].user
        if user.is_anonymous:
            user = None

        data = validated_data.copy()
        data['submitted_by'] = user
        publication = super().create(data)

        for doc_data in docs_data:
            doc_data['submitted_by'] = user
            Document.objects.create(publication=publication, **doc_data)

        return publication

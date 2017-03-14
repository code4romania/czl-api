from django.db import IntegrityError
from rest_framework import serializers, fields
from .models import PUBLICATION_TYPES, Institution, Publication, Document
from .fields import CleansedURLField


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution


class _WritableModelSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('_created_by', '_created_at')


class DocumentSerializer(_WritableModelSerializer):
    url = CleansedURLField()

    class Meta(_WritableModelSerializer.Meta):
        model = Document


class NestedDocumentSerializer(DocumentSerializer):
    class Meta(DocumentSerializer.Meta):
        exclude = ('publication', 'id') + DocumentSerializer.Meta.exclude


class PublicationSerializer(_WritableModelSerializer):
    type = fields.ChoiceField(choices=PUBLICATION_TYPES._doubles)
    documents = NestedDocumentSerializer(many=True, required=False)

    class Meta(_WritableModelSerializer.Meta):
        model = Publication
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        docs_data = validated_data.pop('documents', [])
        user = self.context['request'].user
        if user.is_anonymous:
            user = None

        data = validated_data.copy()
        data['_created_by'] = user
        try:
            publication = super().create(data)
        except IntegrityError as e:
            # err... this is silly but oh well
            err = str(e)
            msg = "Integrity Error"

            # WARNING: this is based on a very specific error format
            # and is quite likely to fail on upgrade
            if err.startswith("duplicate key value violates unique constraint"):
                detail = err.splitlines()[1]
                _intro = 'DETAIL:'
                if detail.startswith(_intro):
                    detail = detail[len(_intro):].strip()

                msg += ": " + detail

            raise serializers.ValidationError(msg)

        for doc_data in docs_data:
            doc_data['_created_by'] = user
            Document.objects.create(publication=publication, **doc_data)

        return publication

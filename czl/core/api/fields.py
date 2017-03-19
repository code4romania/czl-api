from rest_framework import fields
from werkzeug.urls import url_fix

class CleansedURLField(fields.URLField):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return url_fix(data)

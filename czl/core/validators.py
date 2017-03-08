from django.contrib.postgres.validators import KeysValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class AllowedKeysValidator(KeysValidator):
    """A validator that accepts only a set of (optional) keys."""

    message = _('Some unknown keys were provided: %(keys)s')

    def __init__(self, *keys, message=None):
        self.keys = set(keys)
        if message:
            self.message = message

    def __call__(self, value):
        keys = set(value.keys())
        extra_keys = keys - self.keys
        if extra_keys:
            raise ValidationError(
                message,
                code='extra_keys',
                params={'keys': ', '.join(extra_keys)},
            )

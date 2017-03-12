from django.conf import settings
from django.db import models
from django.contrib.postgres import fields as pgfields
from model_utils import Choices
#from .validators import AllowedKeysValidator


PUBLICATION_TYPES = Choices(
    ('LEGE', "Lege"),
    ('HG', "Hotărâre de guvern"),
    ('OG', "Ordonanță de guvern"),
    ('OUG', "Ordonanță de urgență"),
    ('OM', "Ordin de ministru"),
    ('OTHER', "Altceva..."),
)


class Institution(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=256)
    url = models.URLField()

    def __str__(self):
        return self.name


class _WritableModel(models.Model):
    _created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    _created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-_created_at']
        abstract = True


class Publication(_WritableModel):
    ID_FORMAT = "{institution}:{date}:{identifier}"

    __identifier_length = 128
    __id_length = (Institution._meta.get_field('id').max_length
                   + 10 # date
                   + __identifier_length
                   + 2 # separators in ID_FORMAT
    )

    id = models.CharField(max_length=__id_length, primary_key=True)
    identifier = models.CharField(max_length=__identifier_length)
    title = models.CharField(max_length=2048)
    # TODO: switch this to an enum on the db side
    type = models.CharField(PUBLICATION_TYPES, max_length=5)
    institution = models.ForeignKey(Institution)
    date = models.DateField(db_index=True)
    description = models.TextField(blank=True)
    feedback_days = models.PositiveSmallIntegerField(null=True)
    contact = pgfields.HStoreField(default=dict) # (validators=[
    #    AllowedKeysValidator('tel', 'email', 'addr'),
    # ])

    def __str__(self):
        return "%s - %s" % (self.date, self.title)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.ID_FORMAT.format(institution=self.institution.id,
                                            date=self.date.isoformat(),
                                            identifier=self.identifier)
        super().save(*args, **kwargs)


class Document(_WritableModel):
    publication = models.ForeignKey(Publication, related_name="documents")
    type = models.CharField(max_length=128, blank=True)
    url = models.URLField(max_length=2048)

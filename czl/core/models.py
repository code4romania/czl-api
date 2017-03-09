from django.db import models
from django.contrib.postgres import fields as pgfields
from enumfields import EnumField, Enum
from .validators import AllowedKeysValidator


class PUBLICATION_TYPES(Enum):
    PROIECT = "proiect"
    HG = "hg"
    OG = "og"
    OUG = "oug"

    class Labels:
        PROIECT = "Proiect de lege"
        HG = "Hotărâre de guvern"
        OG = "Ordonanță de guvern"
        OUG = "Ordonanță de urgență"


class Institution(models.Model):
    name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=32)
    url = models.URLField()

    def __str__(self):
        return self.name


class Publication(models.Model):
    title = models.CharField(max_length=512)
    # TODO: switch this to an enum on the db side as well
    type = EnumField(PUBLICATION_TYPES, max_length=7)
    issuer = models.ForeignKey(Institution)
    date = models.DateField(db_index=True)
    description = models.TextField()
    feedback_days = models.PositiveSmallIntegerField()
    contact = pgfields.HStoreField(default=dict) # (validators=[
    #    AllowedKeysValidator('tel', 'email', 'addr'),
    # ])

    def __str__(self):
        return "%s - %s" % (self.date, self.title)


class Document(models.Model):
    publication = models.ForeignKey(Publication)
    type = models.CharField(max_length=128, blank=True)
    url = models.URLField()

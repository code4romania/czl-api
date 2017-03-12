from django.conf import settings
from django.db import models
from django.contrib.postgres import fields as pgfields
from enumfields import EnumField, Enum
#from .validators import AllowedKeysValidator


class PUBLICATION_TYPES(Enum):
    LEGE = "lege"
    HG = "hg"
    OG = "og"
    OUG = "oug"
    OM = "om"
    OTHER = "other"

    class Labels:
        LEGE = "Lege"
        HG = "Hotărâre de guvern"
        OG = "Ordonanță de guvern"
        OUG = "Ordonanță de urgență"
        OM = "Ordin de ministru"
        OTHER = "Altceva..."


class Institution(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=256)
    url = models.URLField()

    def __str__(self):
        return self.name


class Publication(models.Model):
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
    # TODO: switch this to an enum on the db side as well
    type = EnumField(PUBLICATION_TYPES, max_length=7)
    institution = models.ForeignKey(Institution)
    date = models.DateField(db_index=True)
    description = models.TextField(blank=True)
    feedback_days = models.PositiveSmallIntegerField(null=True)
    contact = pgfields.HStoreField(default=dict) # (validators=[
    #    AllowedKeysValidator('tel', 'email', 'addr'),
    # ])
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    def __str__(self):
        return "%s - %s" % (self.date, self.title)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.ID_FORMAT.format(institution=self.issuer.id,
                                            date=self.date.isoformat(),
                                            identifier=self.identifier)
        super().save(*args, **kwargs)


class Document(models.Model):
    publication = models.ForeignKey(Publication, related_name="documents")
    type = models.CharField(max_length=128, blank=True)
    url = models.URLField()
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

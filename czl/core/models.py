from datetime import timedelta
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

MINIMUM_FEEDBACK_DAYS = 10


class Institution(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=256)
    url = models.URLField()
    # some institutions advertise a default number of feedback days
    _feedback_days = models.PositiveSmallIntegerField(null=True)

    @property
    def feedback_days(self):
        days = self._feedback_days
        return (MINIMUM_FEEDBACK_DAYS if days is None
                else days)

    @feedback_days.setter
    def feedback_days(self, days):
        self._feedback_days = days

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # if it's the first time we set feedback_days,
        # update this institutions' publications.
        # (the logic being, if feedback_days was previously set then it must be
        # a policy change by the institution, so don't alter past items).

        if self.feedback_days is not None:
            # not the prettiest way to find out if data changed, but oh well
            cls = self.__class__
            try:
                # this might have been just created
                oldself = cls.objects.get(pk=self.pk)
            except cls.DoesNotExist:
                pass
            else:
                if oldself.feedback_days is None:
                    self.update_pub_dates()

        super().save(*args, **kwargs)

    def update_pub_dates(self):
        # update all related publications' max_feedback_date
        # if it was automatically derived
        pubs = self.publication_set().filter(_feedback_days__isnull=True)
        for pub in pubs:
            # just clear the computed value, the model will do the right thing
            pub.max_feedback_date = None
            pub.save()


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
    _feedback_days = models.PositiveSmallIntegerField(null=True)
    max_feedback_date = models.DateField(db_index=True)
    contact = pgfields.HStoreField(default=dict) # (validators=[
    #    AllowedKeysValidator('tel', 'email', 'addr'),
    # ])

    @property
    def feedback_days(self):
        days = self._feedback_days
        if days is not None:
            return days
        if self.institution is None:
            return None
        return self.institution.feedback_days

    @feedback_days.setter
    def feedback_days(self, days):
        self._feedback_days = days

    def __str__(self):
        return "%s - %s" % (self.date, self.title)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.ID_FORMAT.format(institution=self.institution.id,
                                            date=self.date.isoformat(),
                                            identifier=self.identifier)
        if self.max_feedback_date is None:
            self.max_feedback_date = self.date + timedelta(days=self.feedback_days)
        #else if this will ever be updated, we need to update feedback_days too

        super().save(*args, **kwargs)


class Document(_WritableModel):
    publication = models.ForeignKey(Publication, related_name="documents")
    type = models.CharField(max_length=128, blank=True)
    url = models.URLField(max_length=2048)

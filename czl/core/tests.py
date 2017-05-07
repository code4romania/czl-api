# NOTE: the simplest way to run tests is to have the hstore extension available
# in the default template database. as postgres:
# $ echo CREATE EXTENSION hstore | psql template1

import random
from datetime import date, timedelta
from django.test import TestCase

from .models import (
    MINIMUM_FEEDBACK_DAYS, PUBLICATION_TYPES,
    Institution, Publication,
)


class FeedbackDaysTest(TestCase):
    _INSTITUTION_DATA = {
        "id": "test-inst",
        "name": "test institution",
        "url": "http://example.org/"
    }

    _PUBLICATION_DATA = {
        "identifier": "test-pub",
        "title": "test publication",
        "type": random.choice(list(PUBLICATION_TYPES)[0]),
        "date": date.today(),
    }

    @staticmethod
    def get_some_days():
        return random.randint(MINIMUM_FEEDBACK_DAYS + 1,
                              MINIMUM_FEEDBACK_DAYS * 2)

    def test_institution_days_unset(self):
        institution = Institution.objects.create(**self._INSTITUTION_DATA)

        # test that it's been "set" to the default
        self.assertEqual(institution.feedback_days, MINIMUM_FEEDBACK_DAYS)
        # and also test the internal implementation
        self.assertIsNone(institution._feedback_days)

    def test_institution_days_set(self):
        days = self.get_some_days()

        institution = Institution.objects.create(
            feedback_days=days,
            **self._INSTITUTION_DATA
        )

        self.assertEqual(institution.feedback_days, days)
        # and the internal implementation
        self.assertEqual(institution._feedback_days, days)

    def test_publication_days_unset__institution_days_unset(self):
        institution = Institution.objects.create(**self._INSTITUTION_DATA)
        publication = Publication.objects.create(
            institution=institution,
            **self._PUBLICATION_DATA
        )

        self.assertEqual(publication.feedback_days,
                         MINIMUM_FEEDBACK_DAYS)
        self.assertEqual(publication.max_feedback_date,
                         publication.date + timedelta(days=MINIMUM_FEEDBACK_DAYS))
        # and the behind-the-scenes
        self.assertIsNone(publication._feedback_days)

    def test_publication_days_unset__institution_days_set(self):
        days = self.get_some_days()

        institution = Institution.objects.create(
            feedback_days=days,
            **self._INSTITUTION_DATA
        )
        publication = Publication.objects.create(
            institution=institution,
            **self._PUBLICATION_DATA
        )

        self.assertEqual(publication.feedback_days,
                         days)
        self.assertEqual(publication.max_feedback_date,
                         publication.date + timedelta(days=days))
        self.assertIsNone(publication._feedback_days)

    def test_publication_days_set(self):
        institution = Institution.objects.create(**self._INSTITUTION_DATA)
        days = self.get_some_days()

        publication = Publication.objects.create(
            institution=institution,
            feedback_days=days,
            **self._PUBLICATION_DATA
        )

        self.assertEqual(publication.feedback_days,
                         days)
        self.assertEqual(publication.max_feedback_date,
                         publication.date + timedelta(days=days))
        # and most importantly...
        self.assertEqual(publication._feedback_days,
                         days)

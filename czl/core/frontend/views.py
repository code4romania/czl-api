from collections import defaultdict
from datetime import date, timedelta
from django.shortcuts import render
from django.db.models import fields
from django.db.models.aggregates import Count
from django.db.models import expressions as expr
from ..models import (
    DEFAULT_FEEDBACK_DAYS, Institution, Publication,
)

QUERY_PERIOD = 30

def home(request):
    institutions = Institution.objects.annotate(
        pub_count=Count('publication'),
        # probably impossible to do this in a single query
        # with django, but reserving the name here
        open_pub_count=expr.Value(0, fields.IntegerField()),
    ).all()

    # get the open publications in a separate query
    today = date.today()
    open_pubs = dict(
        Publication.objects
        # TODO: these annotations should be in the default query
        .annotate(fbdays=expr.Case(
            expr.When(feedback_days=None,
                      then=DEFAULT_FEEDBACK_DAYS),
            default=expr.F('feedback_days')))
        .annotate(fbmax=expr.ExpressionWrapper(
            expr.F('date') + expr.F('fbdays'),
            output_field=fields.DateField()))
        .filter(
            # in the future date might be null until resolved
            date__isnull=False,
            fbmax__gte=today,
        )
        .order_by() # clears ordering
        .values_list('institution')
        .annotate(count=Count('pk'))
    )

    query_period = today - timedelta(days=QUERY_PERIOD)
    max_count = 0
    _frequencies = (
        Publication.objects.filter(date__gt=query_period)
        .values('institution', 'date')
        .annotate(count=Count('id'))
        .order_by('institution', 'date')
    )
    frequencies = defaultdict(dict)
    for _f in _frequencies:
        count = _f['count']
        frequencies[_f['institution']][_f['date']] = count
        max_count = max(max_count, count)

    period_dates = tuple(today - timedelta(days=x)
                         for x in reversed(range(QUERY_PERIOD)))
    _zeroes = tuple(0 for _d in period_dates)

    # hack the data into the institutions
    for inst in institutions:
        inst.open_pub_count = open_pubs.get(inst.pk, 0)

        if inst.id not in frequencies:
            inst.frequencies = _zeroes
        else:
            inst.frequencies = tuple(
                frequencies[inst.id].get(pdate, 0)
                for pdate in period_dates
            )

    return render(request, 'homepage.html', {
        'institutions': institutions,
        'stats_period': QUERY_PERIOD,
        'max_count': max_count,
    }
)

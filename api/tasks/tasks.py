from datetime import datetime, timedelta
from cryptocurrency.celery import app

from django.db.models import Q


@app.task(acks_late=False)
def add():
    from api.models import Transaction
    from service.bitexen import BitexenService

    try:
        service = BitexenService()
        transactions = service._get_last_transactions()
        Transaction.objects.bulk_create(transactions)
    except Exception as e:
        pass


@app.task(acks_late=False)
def test():
    from api.models import TestReport, Transaction
    from django.db.models import Avg, Max, Min, Sum

    resp = Transaction.objects.all().aggregate(
        max=Max("price"), min=Min("price"), avg=Avg("price"), total=Sum("price")
    )
    TestReport.objects.create(
        max_val=resp.get("max"),
        min_val=resp.get("min"),
        avg_val=resp.get("avg"),
        total_val=resp.get("total"),
    )


@app.task(acks_late=False)
def daily():
    from api.models import DailyReport, Transaction
    from django.db.models import Avg, Max, Min, Sum

    resp = Transaction.objects.all().aggregate(
        max=Max("price"), min=Min("price"), avg=Avg("price"), total=Sum("price")
    )
    DailyReport.objects.create(
        max_val=resp.get("max"),
        min_val=resp.get("min"),
        avg_val=resp.get("avg"),
        total_val=resp.get("total"),
    )


@app.task(acks_late=False)
def weekly():
    from api.models import WeeklyReport, Transaction
    from django.db.models import Avg, Max, Min, Sum

    _to = datetime.now()
    _from = _to - timedelta(days=7)
    _filter = Q(created_at__gte=_from, created_at__lte=_to)

    resp = Transaction.objects.filter(_filter).aggregate(
        max=Max("price"), min=Min("price"), avg=Avg("price"), total=Sum("price")
    )
    WeeklyReport.objects.create(
        max_val=resp.get("max"),
        min_val=resp.get("min"),
        avg_val=resp.get("avg"),
        total_val=resp.get("total"),
    )


@app.task(acks_late=False)
def monthly():
    from api.models import MonthlyReport, Transaction
    from django.db.models import Avg, Max, Min, Sum

    _to = datetime.now()
    _from = _to - timedelta(days=30)
    _filter = Q(created_at__gte=_from, created_at__lte=_to)

    resp = Transaction.objects.filter(_filter).aggregate(
        max=Max("price"), min=Min("price"), avg=Avg("price"), total=Sum("price")
    )
    MonthlyReport.objects.create(
        max_val=resp.get("max"),
        min_val=resp.get("min"),
        avg_val=resp.get("avg"),
        total_val=resp.get("total"),
    )

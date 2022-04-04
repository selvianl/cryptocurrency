from datetime import datetime, timedelta

from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view

from api.models import TestReport


@api_view(["GET"])
def get_daily_report(request, date):
    """
    Date format has to be given
    YYYY-MM-DD like 2022-04-03
    """
    try:
        _from = datetime.strptime(date, "%Y-%m-%d")
        _to = _from + timedelta(1)
        _filter = Q(created_at__gte=_from, created_at__lte=_to)
        qs = TestReport.objects.filter(_filter).first()
        if qs:
            data = {
                "min_val": qs.min_val,
                "max_val": qs.max_val,
                "avg_val": qs.avg_val,
                "total_val": qs.total_val,
            }
            return JsonResponse(data)
        return JsonResponse({"message": "No data yet"})
    except ValueError:
        return JsonResponse({"message": "Date Format is not valid"})
    except Exception:
        return JsonResponse({"message": "Error"})

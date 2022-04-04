from django.urls import path
from api.views import get_daily_report

urlpatterns = [path("daily_report/<str:date>/", get_daily_report, name="daily_report")]

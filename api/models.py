from django.db import models


class CoreModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name="Updated At"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    is_deleted = models.BooleanField(default=False, verbose_name="Is Deleted")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Deleted At")
    data = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True
        ordering = ["-id"]


class Transaction(CoreModel):
    amount = models.CharField(max_length=250, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    time = models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        ordering = ["-id"]


class BaseReport(CoreModel):
    max_val = models.FloatField(null=True, blank=True)
    min_val = models.FloatField(null=True, blank=True)
    avg_val = models.FloatField(null=True, blank=True)
    total_val = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["-id"]


class TestReport(BaseReport):
    pass


class DailyReport(BaseReport):
    pass


class WeeklyReport(BaseReport):
    pass


class MonthlyReport(BaseReport):
    pass

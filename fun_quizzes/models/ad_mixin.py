from django.db import models

class AdMixin(models.Model):
    ad_shown = models.BooleanField(default=False, verbose_name="광고 노출 여부")
    ad_shown_at = models.DateTimeField(null=True, blank=True, verbose_name="광고 노출 시간")

    class Meta:
        abstract = True
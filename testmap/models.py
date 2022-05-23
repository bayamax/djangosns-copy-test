from django.contrib.auth import get_user_model
from django.contrib.gis.db import models

class Border(models.Model):
    id      = models.AutoField(primary_key=True)
    n03_001 = models.CharField(verbose_name='都道府県名', max_length=10)
    n03_002 = models.CharField(verbose_name='支庁名', max_length=20, blank=True)
    n03_003 = models.CharField(verbose_name='群・政令市名', max_length=20, blank=True)
    n03_004 = models.CharField(verbose_name='市区町村名', max_length=20, blank=True)
    n03_007 = models.CharField(verbose_name='行政区域コード', max_length=5)
    geom = models.PolygonField(srid=4612)
    objects = models.Manager()

    def __str__(self):
        return "%s_%s_%s" % (self.n03_001,self.n03_003,self.n03_004)

    class Meta:
        verbose_name = "行政区域"
        verbose_name_plural = "行政区域一覧"
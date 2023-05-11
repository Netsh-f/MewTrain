from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="站名")
    city = models.CharField(max_length=128, verbose_name="城市")

    def __str__(self):
        return '<id=%s> %s' % (self.id, self.name)

    class Meta:
        verbose_name = '车站'
        verbose_name_plural = '车站'
        ordering = ['-name']


class Train(models.Model):
    type_choices = (
        ('HS', '高铁'),
        ('regular', '普通车'),
    )

    name = models.CharField(max_length=128, unique=True, verbose_name="车次")
    type = models.CharField(max_length=8, choices=type_choices, default="HS", verbose_name="车次类型")

    def __str__(self):
        return '<id=%s> %s' % (self.id, self.name)

    class Meta:
        verbose_name = '列车'
        verbose_name_plural = '列车'
        ordering = ['-name']

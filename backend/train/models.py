from django.db import models
from decimal import Decimal

from user.models import User


class Station(models.Model):
    name = models.CharField(max_length=5, unique=True, verbose_name="车站名", null=False)
    code = models.CharField(max_length=3, unique=True, verbose_name="车站代码", null=False)
    city = models.CharField(max_length=10, verbose_name="城市名", null=False)

    class Meta:
        verbose_name = '车站'
        verbose_name_plural = '车站'
        ordering = ['-station_num']


class Train(models.Model):
    train_type_choices = (
        ('HSR', '高铁'),
        ('REG', '普通车'),
    )

    name = models.CharField(max_length=128, unique=True, verbose_name="车次", null=False)
    train_type = models.CharField(max_length=8, choices=train_type_choices, default="HSR", verbose_name="车次类型",
                                  null=False)
    departure_time = models.DateTimeField(verbose_name='出发日期')

    class Meta:
        verbose_name = '列车'
        verbose_name_plural = '列车'
        ordering = ['-name']


class Stop(models.Model):
    train = models.ForeignKey(Train, verbose_name='车次', on_delete=models.CASCADE, null=False)
    station = models.ForeignKey(Station, verbose_name='车站', on_delete=models.CASCADE, null=False)
    arrival_time = models.TimeField(verbose_name='到达时间')
    duration = models.DurationField(verbose_name='停留时间')
    # 出发时间根据上面两项计算，以处理跨天的情况
    sequence = models.IntegerField(verbose_name='序号', null=False)

    class Meta:
        verbose_name = '途径站'
        verbose_name_plural = '途径站'
        ordering = ['-id']


class Carriage(models.Model):
    TYPE_CHOICES = (
        ('BUS', '商务舱'),
        ('FST', '一等舱'),
        ('SND', '二等舱'),
        ('SOF', '软卧'),
        ('HAW', '硬卧'),
        ('HAZ', '硬座'),
    )

    carriage_num = models.PositiveSmallIntegerField(verbose_name='车厢号')
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, verbose_name='车厢类型')
    total_num = models.PositiveSmallIntegerField(verbose_name='座位总数')
    total_available = models.PositiveSmallIntegerField(verbose_name='剩余座位数')
    seats = models.JSONField(default=dict, verbose_name='座位分布')
    train = models.ForeignKey(Train, on_delete=models.CASCADE, verbose_name='所属车次')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='价格')

    class Meta:
        verbose_name = '车厢'
        verbose_name_plural = '车厢'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if not self.seats:
            self.seats = {
                'A': 0,
                'B': 0,
                'C': 0,
                'D': 0,
                'F': 0,
            }
        super().save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE, null=False)
    train = models.ForeignKey(Train, verbose_name='车次', on_delete=models.CASCADE, null=False)
    carriage_num = models.PositiveSmallIntegerField(verbose_name='车厢号')
    seat_num = models.CharField(max_length=3, verbose_name='座位位置')
    departure_station = models.ForeignKey(Stop, verbose_name='出发站', related_name='arrivals',
                                          on_delete=models.CASCADE)
    departure_time = models.DateTimeField(verbose_name='出发时间')
    arrival_station = models.ForeignKey(Stop, verbose_name='到达站', related_name='departures',
                                        on_delete=models.CASCADE)
    arrival_time = models.DateTimeField(verbose_name='到达时间')
    create_time = models.DateTimeField(verbose_name='创建时间', null=False)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-id']

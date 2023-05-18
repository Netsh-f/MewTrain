from django.db import models
from decimal import Decimal

from user.models import User


class Station(models.Model):
    name = models.CharField(max_length=5, unique=True, verbose_name="车站名", null=False)
    code = models.CharField(max_length=3, unique=True, verbose_name="车站代码", null=False)
    station_num = models.PositiveSmallIntegerField(unique=True, verbose_name="车站编号")
    city_num = models.PositiveSmallIntegerField(verbose_name="城市编号")
    city_name = models.CharField(max_length=10, verbose_name="城市名", null=False)

    def __str__(self):
        return '<id=%s> %s' % (self.id, self.name)

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

    def __str__(self):
        return '<id=%s> %s' % (self.id, self.name)

    class Meta:
        verbose_name = '列车'
        verbose_name_plural = '列车'
        ordering = ['-name']


class Seat(models.Model):
    seat_type_choices = (
        ('business', '商务座'),
        ('first', '一等座'),
        ('second', '二等座'),
        ('hardSleeper', '硬卧'),
        ('softSleeper', '软卧'),
        ('noSeat', '无座'),
        ('hardSeat', '硬座'),
    )

    train = models.ForeignKey(Train, on_delete=models.CASCADE, verbose_name='车次', null=False)
    carriage = models.PositiveSmallIntegerField(verbose_name='车厢号', null=False)
    seat_type = models.CharField(max_length=16, choices=seat_type_choices, default='second', verbose_name='座位类型',
                                 null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='价格')
    location = models.CharField(max_length=4, verbose_name='位置', null=False)
    is_available = models.BooleanField(verbose_name='是否可用')

    def __str__(self):
        return '<id=%s> %s %s' % (self.id, self.train_id, self.location)

    class Meta:
        verbose_name = '座位'
        verbose_name_plural = '座位'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['train_id', 'carriage', 'location'],
                                    name='unique_train_id_carriage_location')
        ]


class Stop(models.Model):
    train = models.ForeignKey(Train, verbose_name='车次', on_delete=models.CASCADE, null=False)
    station = models.ForeignKey(Station, verbose_name='车站', on_delete=models.CASCADE, null=False)
    arrival_time = models.TimeField(verbose_name='到达时间')
    duration = models.DurationField(verbose_name='停留时间')
    # 出发时间根据上面两项计算，以处理跨天的情况
    sequence = models.IntegerField(verbose_name='序号', null=False)

    def __str__(self):
        return '<id=%s> train=%s station=%s %s %s' % (
            self.id, self.train_id, self.station_id, self.arrival_time, self.departureTime)

    class Meta:
        verbose_name = '途径站'
        verbose_name_plural = '途径站'
        ordering = ['-id']


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE, null=False)
    train = models.ForeignKey(Train, verbose_name='车次', on_delete=models.CASCADE, null=False)
    seat = models.ForeignKey(Seat, verbose_name='座位', on_delete=models.CASCADE, null=False)
    departure_station = models.ForeignKey(Stop, verbose_name='出发站', related_name='arrivals',
                                          on_delete=models.CASCADE)
    departure_time = models.DateTimeField(verbose_name='出发时间')
    arrival_station = models.ForeignKey(Stop, verbose_name='到达站', related_name='departures',
                                        on_delete=models.CASCADE)
    arrival_time = models.DateTimeField(verbose_name='到达时间')
    create_time = models.DateTimeField(verbose_name='创建时间', null=False)

    def __str__(self):
        return '<id=%s> train=%s station=%s seat=%s %s %s' % (
            self.id, self.train_id, self.station_id, self.seat_id, self.departure_station, self.arrival_station)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-id']

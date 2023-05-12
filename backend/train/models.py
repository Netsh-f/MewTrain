from django.db import models
from decimal import Decimal

from user.models import User


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
    train_type_choices = (
        ('HS', '高铁'),
        ('regular', '普通车'),
    )

    name = models.CharField(max_length=128, unique=True, verbose_name="车次")
    train_type = models.CharField(max_length=8, choices=train_type_choices, default="HS", verbose_name="车次类型")

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

    train_id = models.ForeignKey(Train, on_delete=models.CASCADE, verbose_name='车次')
    carriage = models.IntegerField(verbose_name='车厢号')
    seat_type = models.CharField(max_length=16, choices=seat_type_choices, default='second', verbose_name='座位类型')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='价格')
    location = models.CharField(max_length=4, verbose_name='位置')

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


class PassingStation(models.Model):
    train_id = models.ForeignKey(Train, verbose_name='车次')
    station_id = models.ForeignKey(Station, verbose_name='车站')
    arrival_time = models.DateTimeField(datetime_format='%Y-%m-%d %H:%M', verbose_name='到达时间')
    departureTime = models.DateTimeField(datetime_format='%Y-%m-%d %H:%M', verbose_name='出发时间')

    @property
    def stop_time(self):
        return self.departureTime - self.arrival_time

    def __str__(self):
        return '<id=%s> train=%s station=%s %s %s' % (
            self.id, self.train_id, self.station_id, self.arrival_time, self.departureTime)

    class Meta:
        verbose_name = '途径站'
        verbose_name_plural = '途径站'
        ordering = ['-id']


class Order(models.Model):
    user_id = models.ForeignKey(User, verbose_name='用户')
    train_id = models.ForeignKey(Train, verbose_name='车次')
    seat_id = models.ForeignKey(Seat, verbose_name='座位')
    departure_station = models.ForeignKey(PassingStation, verbose_name='出发站')
    arrival_station = models.ForeignKey(PassingStation, verbose_name='到达站')
    create_time = models.DateTimeField(verbose_name='创建时间')

    def __str__(self):
        return '<id=%s> train=%s station=%s seat=%s %s %s' % (
            self.id, self.train_id, self.station_id, self.seat_id, self.departure_station, self.arrival_station)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-id']

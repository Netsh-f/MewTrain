# Generated by Django 4.2 on 2023-05-15 15:05

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Station",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pinyin_3", models.CharField(max_length=3, verbose_name="拼音3字母简写")),
                (
                    "name",
                    models.CharField(max_length=5, unique=True, verbose_name="车站名"),
                ),
                (
                    "code",
                    models.CharField(max_length=3, unique=True, verbose_name="车站代码"),
                ),
                ("pinyin_full", models.CharField(max_length=18, verbose_name="拼音全称")),
                ("pinyin_head", models.CharField(max_length=5, verbose_name="拼音首字母简写")),
                (
                    "station_num",
                    models.PositiveSmallIntegerField(unique=True, verbose_name="车站编号"),
                ),
                ("city_num", models.PositiveSmallIntegerField(verbose_name="城市编号")),
                ("city_name", models.CharField(max_length=10, verbose_name="城市名")),
            ],
            options={
                "verbose_name": "车站",
                "verbose_name_plural": "车站",
                "ordering": ["-station_num"],
            },
        ),
        migrations.CreateModel(
            name="Train",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=128, unique=True, verbose_name="车次"),
                ),
                (
                    "train_type",
                    models.CharField(
                        choices=[("HSR", "高铁"), ("REG", "普通车")],
                        default="HSR",
                        max_length=8,
                        verbose_name="车次类型",
                    ),
                ),
            ],
            options={
                "verbose_name": "列车",
                "verbose_name_plural": "列车",
                "ordering": ["-name"],
            },
        ),
        migrations.CreateModel(
            name="Stop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("arrival_time", models.TimeField(verbose_name="到达时间")),
                ("duration", models.DurationField(verbose_name="停留时间")),
                ("sequence", models.IntegerField(verbose_name="序号")),
                (
                    "station_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="train.station",
                        verbose_name="车站",
                    ),
                ),
                (
                    "train_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="train.train",
                        verbose_name="车次",
                    ),
                ),
            ],
            options={
                "verbose_name": "途径站",
                "verbose_name_plural": "途径站",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Seat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("carriage", models.PositiveSmallIntegerField(verbose_name="车厢号")),
                (
                    "seat_type",
                    models.CharField(
                        choices=[
                            ("business", "商务座"),
                            ("first", "一等座"),
                            ("second", "二等座"),
                            ("hardSleeper", "硬卧"),
                            ("softSleeper", "软卧"),
                            ("noSeat", "无座"),
                            ("hardSeat", "硬座"),
                        ],
                        default="second",
                        max_length=16,
                        verbose_name="座位类型",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0.00"),
                        max_digits=8,
                        verbose_name="价格",
                    ),
                ),
                ("location", models.CharField(max_length=4, verbose_name="位置")),
                ("is_available", models.BooleanField(verbose_name="是否可用")),
                (
                    "train_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="train.train",
                        verbose_name="车次",
                    ),
                ),
            ],
            options={
                "verbose_name": "座位",
                "verbose_name_plural": "座位",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("departure_time", models.DateTimeField(verbose_name="出发时间")),
                ("arrival_time", models.DateTimeField(verbose_name="到达时间")),
                ("create_time", models.DateTimeField(verbose_name="创建时间")),
                (
                    "arrival_station",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="departures",
                        to="train.stop",
                        verbose_name="到达站",
                    ),
                ),
                (
                    "departure_station",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="arrivals",
                        to="train.stop",
                        verbose_name="出发站",
                    ),
                ),
                (
                    "seat_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="train.seat",
                        verbose_name="座位",
                    ),
                ),
                (
                    "train_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="train.train",
                        verbose_name="车次",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.user",
                        verbose_name="用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "订单",
                "verbose_name_plural": "订单",
                "ordering": ["-id"],
            },
        ),
        migrations.AddConstraint(
            model_name="seat",
            constraint=models.UniqueConstraint(
                fields=("train_id", "carriage", "location"),
                name="unique_train_id_carriage_location",
            ),
        ),
    ]

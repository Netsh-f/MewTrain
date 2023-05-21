# Generated by Django 4.2 on 2023-05-20 20:51

import datetime
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("train", "0002_rename_seat_id_order_seat_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Carriage",
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
                ("carriage_num", models.PositiveSmallIntegerField(verbose_name="车厢号")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("BUS", "商务舱"),
                            ("FST", "一等舱"),
                            ("SND", "二等舱"),
                            ("SOF", "软卧"),
                            ("HAW", "硬卧"),
                            ("HAZ", "硬座"),
                        ],
                        max_length=3,
                        verbose_name="车厢类型",
                    ),
                ),
                ("total_num", models.PositiveSmallIntegerField(verbose_name="座位总数")),
                (
                    "total_available",
                    models.PositiveSmallIntegerField(verbose_name="剩余座位数"),
                ),
                ("seats", models.JSONField(default=dict, verbose_name="座位分布")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0.00"),
                        max_digits=8,
                        verbose_name="价格",
                    ),
                ),
            ],
            options={
                "verbose_name": "车厢",
                "verbose_name_plural": "车厢",
                "ordering": ["-id"],
            },
        ),
        migrations.AlterModelOptions(
            name="station",
            options={
                "ordering": ["-id"],
                "verbose_name": "车站",
                "verbose_name_plural": "车站",
            },
        ),
        migrations.AlterModelOptions(
            name="train",
            options={
                "ordering": ["-id"],
                "verbose_name": "列车",
                "verbose_name_plural": "列车",
            },
        ),
        migrations.RenameField(
            model_name="station",
            old_name="city_name",
            new_name="city",
        ),
        migrations.RemoveField(
            model_name="order",
            name="seat",
        ),
        migrations.RemoveField(
            model_name="station",
            name="city_num",
        ),
        migrations.RemoveField(
            model_name="station",
            name="pinyin_3",
        ),
        migrations.RemoveField(
            model_name="station",
            name="pinyin_full",
        ),
        migrations.RemoveField(
            model_name="station",
            name="pinyin_head",
        ),
        migrations.RemoveField(
            model_name="station",
            name="station_num",
        ),
        migrations.AddField(
            model_name="order",
            name="carriage_num",
            field=models.PositiveSmallIntegerField(default=0, verbose_name="车厢号"),
        ),
        migrations.AddField(
            model_name="order",
            name="seat_num",
            field=models.CharField(default=0, max_length=3, verbose_name="座位位置"),
        ),
        migrations.AddField(
            model_name="train",
            name="departure_time",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 5, 20, 8, 0), verbose_name="出发日期"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="departure_time",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 5, 20, 8, 0), verbose_name="出发时间"
            ),
        ),
        migrations.DeleteModel(
            name="Seat",
        ),
        migrations.AddField(
            model_name="carriage",
            name="train",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="train.train",
                verbose_name="所属车次",
            ),
        ),
    ]
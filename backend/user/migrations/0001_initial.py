# Generated by Django 4.2 on 2023-06-07 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AbstractUser",
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
                    "username",
                    models.CharField(max_length=128, unique=True, verbose_name="用户名"),
                ),
                ("password", models.CharField(max_length=256, verbose_name="密码")),
            ],
        ),
        migrations.CreateModel(
            name="RailwayAdmin",
            fields=[
                (
                    "abstractuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="user.abstractuser",
                    ),
                ),
            ],
            options={
                "verbose_name": "铁路系统员",
                "verbose_name_plural": "铁路系统员",
                "ordering": ["-id"],
            },
            bases=("user.abstractuser",),
        ),
        migrations.CreateModel(
            name="SystemAdmin",
            fields=[
                (
                    "abstractuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="user.abstractuser",
                    ),
                ),
            ],
            options={
                "verbose_name": "系统管理员",
                "verbose_name_plural": "系统管理员",
                "ordering": ["-id"],
            },
            bases=("user.abstractuser",),
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "abstractuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="user.abstractuser",
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, null=True, verbose_name="邮箱地址"),
                ),
                (
                    "balance",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
            ],
            options={
                "verbose_name": "用户",
                "verbose_name_plural": "用户",
                "ordering": ["-id"],
            },
            bases=("user.abstractuser",),
        ),
        migrations.CreateModel(
            name="Passenger",
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
                    "id_type",
                    models.CharField(
                        choices=[
                            ("CIC", "中国居民身份证"),
                            ("HTP", "港澳居民来往内地通行证"),
                            ("TTP", "台湾居民来往大陆通行证"),
                            ("PSP", "护照"),
                            ("FRI", "外国人永久居留身份证"),
                            ("HMT", "港澳台居民居住证"),
                        ],
                        default="chinese_id_card",
                        max_length=3,
                        verbose_name="证件类型",
                    ),
                ),
                ("name", models.CharField(max_length=128, verbose_name="姓名")),
                ("id_number", models.CharField(max_length=32, verbose_name="证件号码")),
                (
                    "ticket_type",
                    models.CharField(
                        choices=[
                            ("ADU", "成人"),
                            ("CHI", "儿童"),
                            ("STU", "学生"),
                            ("DOM", "残军"),
                        ],
                        default="adult",
                        max_length=3,
                        verbose_name="优惠(待)类型",
                    ),
                ),
                (
                    "phone_region",
                    models.CharField(
                        choices=[
                            ("86", "+86"),
                            ("852", "+852"),
                            ("853", "+853"),
                            ("886", "+886"),
                        ],
                        default="86",
                        max_length=3,
                        verbose_name="地区",
                    ),
                ),
                ("phone_number", models.CharField(max_length=32, verbose_name="手机号码")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.user",
                        verbose_name="关联用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "乘车人",
                "verbose_name_plural": "乘车人",
                "ordering": ["-id"],
            },
        ),
    ]

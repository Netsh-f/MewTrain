from django.db import models


class AbstractUser(models.Model):
    username = models.CharField(max_length=128, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=256, verbose_name="密码")

    def __str__(self):
        return '<id=%s> %s' % (self.id, self.username)


class User(AbstractUser):
    email = models.EmailField(null=True, verbose_name="邮箱地址")

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-id']


class Passenger(models.Model):
    id_type_choices = (
        ('chinese_id_card', '中国居民身份证'),
        ('hkm_travel_permit', '港澳居民来往内地通行证'),
        ('taiwan_travel_permit', '台湾居民来往大陆通行证'),
        ('passport', '护照'),
        ('foreign_resident_id', '外国人永久居留身份证'),
        ('hmt_residence_permit', '港澳台居民居住证'),
    )

    ticket_type_choices = (
        ('adult', '成人'),
        ('child', '儿童'),
        ('student', '学生'),
        ('DM', '残军'),
    )

    phone_region_choices = (
        ('86', '+86'),
        ('852', '+852'),
        ('853', '+853'),
        ('886', '+886'),
    )

    id_type = models.CharField(max_length=32, choices=id_type_choices, default='chinese_id_card',
                               verbose_name="证件类型")
    name = models.CharField(max_length=128, verbose_name="姓名")
    id_number = models.CharField(max_length=32, verbose_name="证件号码")
    ticket_type = models.CharField(max_length=16, choices=ticket_type_choices, default='adult',
                                   verbose_name="优惠(待)类型")
    phone_region = models.CharField(max_length=8, choices=phone_region_choices, default='86', verbose_name="地区")
    phone_number = models.CharField(max_length=32, verbose_name="手机号码")
    user_id = models.ForeignKey(User, verbose_name='关联用户', on_delete=models.CASCADE)

    def __str__(self):
        return '<id=%s> %s' % (self.id, self.name)

    class Meta:
        verbose_name = '乘车人'
        verbose_name_plural = '乘车人'
        ordering = ['-id']


class SystemAdmin(AbstractUser):
    class Meta:
        verbose_name = '系统管理员'
        verbose_name_plural = '系统管理员'
        ordering = ['-id']


class RailwayAdmin(AbstractUser):
    class Meta:
        verbose_name = '铁路系统员'
        verbose_name_plural = '铁路系统员'
        ordering = ['-id']

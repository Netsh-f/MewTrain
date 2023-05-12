from django.db import models


class User(models.Model):
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

    username = models.CharField(max_length=128, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=256, verbose_name="密码")
    id_type = models.CharField(max_length=32, choices=id_type_choices, default='chinese_id_card',
                               verbose_name="证件类型")
    name = models.CharField(max_length=128, verbose_name="姓名")
    id_number = models.CharField(max_length=32, verbose_name="证件号码")
    ticket_type = models.CharField(max_length=16, choices=ticket_type_choices, default='adult',
                                   verbose_name="优惠(待)类型")
    phone_region = models.CharField(max_length=8, choices=phone_region_choices, default='86', verbose_name="地区")
    phone_number = models.CharField(max_length=32, verbose_name="手机号码")
    email = models.EmailField(unique=True, null=True, verbose_name="邮箱地址")

    def __str__(self):
        return '<id=%s> %s' % (self.id, self.name)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-id']


class Admin(models.Model):
    admin_type_choices = (
        ('systemAdmin', '系统管理员'),
        ('railwayAdmin', '铁路系统员'),
    )

    username = models.CharField(max_length=128, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=256, verbose_name="密码")
    admin_type = models.CharField(max_length=16, choices=admin_type_choices, default='systemAdmin',
                                  verbose_name='管理员类型')

    def __str__(self):
        return '<id=%s> %s %s' % (self.id, self.admin_type, self.username)

    class Meta:
        verbose_name = '管理员'
        verbose_name_plural = '管理员'
        ordering = ['-id']

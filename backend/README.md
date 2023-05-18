这里是后端目录

developing~

# 接口文档

## 注册普通用户

请求地址：`/user/register/`

请求方式：POST

参数说明：

Body

| 参数                 | 类型     | 必须  | 说明                                                                                                                      |
| ------------------ | ------ | --- | ----------------------------------------------------------------------------------------------------------------------- |
| username           | string | 是   | 用户名                                                                                                                     |
| password           | string | 是   | 密码                                                                                                                      |
| confirmed_password | string | 是   | 确认密码                                                                                                                    |
| email              | string | 否   | 电子邮箱                                                                                                                    |
| id_type            |        | 是   | 证件类型('CIC', '中国居民身份证')('HTP', '港澳居民来往内地通行证')('TTP', '台湾居民来往大陆通行证')('PSP', '护照')('FRI', '外国人永久居留身份证')('HMT', '港澳台居民居住证') |
| name               |        | 是   | 姓名                                                                                                                      |
| id_number          |        | 是   | 证件号                                                                                                                     |
| ticket_type        |        | 是   | 优惠（待）类型('ADU', '成人')('CHI', '儿童')('STU', '学生')('DOM', '残军')                                                             |
| phone_region       |        | 是   | 手机号码地区('86', '+86')('852', '+852')('853', '+853')('886', '+886')                                                        |
| phone_number       |        | 是   | 手机号码                                                                                                                    |

示例：

```json
{
    "username":"Elaikona",
    "password":"123456",
    "confirmed_password":"123456",
    "email":"21371193@buaa.edu.cn",
    "id_type":"CIC",
    "name":"张文津",
    "id_number":"370403199904041234",
    "ticket_type":"STU",
    "phone_region":"86",
    "phone_number":"13869439177"
}
```

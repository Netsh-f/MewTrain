from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response

from user.models import User, Passenger, SystemAdmin, RailwayAdmin


@api_view(['POST'])
def register(request):
    try:
        data = request.data
        username = data['username']

        same_name_user = User.objects.filter(username=username)
        if same_name_user:
            message = '用户名已存在'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        user = User()
        user.username = username
        user.password = make_password(data['password'])
        user.email = data['email']
        user.save()

        message = '用户注册成功'
        return Response({'message': message}, status=status.HTTP_201_CREATED)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_passenger(request):
    try:
        identity = request.session.get('identity', None)
        if identity != 'user' and identity != 'system_admin':
            message = '无效权限'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        user_id = data['user_id']
        user = User.objects.get(id=user_id)
        passenger = Passenger(
            id_type=data['id_type'],
            name=data['name'],
            id_number=data['id_number'],
            ticket_type=data['ticket_type'],
            phone_region=data['phone_region'],
            phone_number=data['phone_number'],
        )
        passenger.user = user
        passenger.save()
        message = '添加乘车员成功'
        return Response({'message': message}, status=status.HTTP_201_CREATED)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login(request):
    try:
        if request.session.get('is_login', None):
            message = '不允许重复登录'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(Q(username=username) | Q(username=username) | Q(username=username))
        except (User.DoesNotExist, SystemAdmin.DoesNotExist, RailwayAdmin.DoesNotExist):
            message = '用户不存在'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        if check_password(password, user.password):
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            if isinstance(user, SystemAdmin):
                request.session['identity'] = 'system_admin'
            elif isinstance(user, RailwayAdmin):
                request.session['identity'] = 'railway_admin'
            else:
                request.session['identity'] = 'user'
            message = '登录成功'
            return Response({'message': message}, status=status.HTTP_200_OK)
        else:
            message = '用户名或密码错误'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def logout(request):
    try:
        if not request.session.get('is_login', None):
            message = '请先登录'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        request.session.flush()
        message = '登出成功'
        return Response({'message': message}, status=status.HTTP_200_OK)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_user_list(request):
    try:
        if request.session.get('identity', None) != 'system_admin':
            message = '请先登录系统管理员账户'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.all().values()
        system_admins = SystemAdmin.objects.all().values()
        railway_admins = RailwayAdmin.objects.all().values()

        user_data = list(users)
        system_admin_data = list(system_admins)
        railway_admin_data = list(railway_admins)

        message = '获取用户列表成功'
        response_data = {
            'message': message,
            'users': user_data,
            'system_admins': system_admin_data,
            'railway_admins': railway_admin_data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_user(request):
    try:
        if request.session.get('identity', None) != 'system_admin':
            message = '请先登录系统管理员账户'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        user_type = data.get('user_type')

        if user_type == 'user':
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            # 创建 User 模型对象
            user = User.objects.create(
                username=username,
                password=password,
                email=email
            )

        elif user_type == 'system_admin':
            username = data.get('username')
            password = data.get('password')

            # 创建 SystemAdmin 模型对象
            system_admin = SystemAdmin.objects.create(
                username=username,
                password=password
            )

        elif user_type == 'railway_admin':
            username = data.get('username')
            password = data.get('password')

            # 创建 RailwayAdmin 模型对象
            railway_admin = RailwayAdmin.objects.create(
                username=username,
                password=password
            )

        else:
            message = '无效的用户类型'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        message = '添加用户成功'
        return Response({'message': message}, status=status.HTTP_201_CREATED)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response

from user.models import User, Passenger


@api_view(['POST'])
def register(request):
    try:
        data = request.data
        username = data['username']
        password = data['password']
        confirmed_password = data['confirmed_password']

        if password != confirmed_password:
            message = '两次输入的密码不同'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        same_name_user = User.objects.filter(username=username)
        if same_name_user:
            message = '用户名已存在'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        user = User()
        user.username = username
        user.password = make_password(password)
        if 'email' in data and data['email']:
            user.email = data['email']

        passenger = Passenger(
            id_type=data['id_type'],
            name=data['name'],
            id_number=data['id_number'],
            ticket_type=data['ticket_type'],
            phone_region=data['phone_region'],
            phone_number=data['phone_number'],
        )
        passenger.user = user
        user.save()
        passenger.save()
        message = '用户注册成功'
        return Response({'message': message}, status=status.HTTP_201_CREATED)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

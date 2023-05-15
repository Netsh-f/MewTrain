from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response

from user.models import User, Passenger


@api_view(['POST'])
def register(request):
    data = request.data
    message = '请检查填写内容'
    username = data['username']

    same_name_user = User.objects.filter(username=username)
    if same_name_user:
        message = '用户名已存在'
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

    user = User()
    user.username = username
    user.password = make_password(data['password'])
    if 'email' in data and data['email']:
        user.email = data['email']
    user.save()

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
    message = '用户注册成功'

    return Response({'message': message}, status=status.HTTP_201_CREATED)

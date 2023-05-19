from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .models import Station


@api_view(['POST'])
def add_station(request):
    try:
        # 检查用户身份
        identity = request.session.get('identity', None)
        if identity != 'system_admin':
            message = '无效权限'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        # 获取请求体中的数据
        data = request.data
        name = data['name']
        code = data['code']
        city = data['city']

        # 创建车站
        station = Station(name=name, code=code, city=city)
        station.save()

        message = '车站添加成功'
        return Response({'message': message}, status=status.HTTP_201_CREATED)

    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_train(request):
    try:
        identity = request.session.get('identity', None)
        if identity != 'system_admin':
            message = '无效权限'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

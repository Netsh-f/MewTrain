from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .models import Station, Train, Carriage, Stop


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
        data = request.data
        train_name = data.get("train_name")
        departure_time = data.get("departure_time")
        train_type = data.get("train_type")
        carriages = data.get("carriages")
        stops = data.get("stops")

        train = Train.objects.create(
            train_name=train_name,
            departure_time=departure_time,
            train_type=train_type
        )

        for carriage_data in carriages:
            carriage_num = carriage_data.get("carriage_num")
            total_num = carriage_data.get("total_num")
            price = carriage_data.get("price")
            seats = carriage_data.get("seats")

            carriage = Carriage.objects.create(
                carriage_num=carriage_num,
                total_num=total_num,
                price=price,
                train=train,
                seats=seats
            )

        for stop_data in stops:
            station_name = stop_data.get("station_name")
            arrival_time = stop_data.get("arrival_time")
            duration = stop_data.get("duration")
            sequence = stop_data.get("sequence")

            # 获取对应的站点对象
            station = Station.objects.get(name=station_name)
            stop = Stop.objects.create(
                station=station,
                train=train,
                arrival_time=arrival_time,
                duration=duration,
                sequence=sequence
            )

        message = '列车添加成功'
        return Response({'message': message}, status=status.HTTP_201_CREATED)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_info(request):
    datas = {
        "name": "MewTrain",
        "staff": [
            "GongYihui",
            "ZhangWenjin",
            "WangXi",
            "WangZishen",
            "YouShibo"
        ]
    }
    message = '你好，前端'
    return Response({'message': message, 'datas': datas}, status=status.HTTP_200_OK)

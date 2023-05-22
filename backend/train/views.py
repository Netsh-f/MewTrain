from datetime import datetime, timedelta

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .models import Station, Train, Carriage, Stop, Ticket


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
        train_type = data.get("train_type")
        carriages = data.get("carriages")
        stops = data.get("stops")

        train = Train.objects.create(
            train_name=train_name,
            train_type=train_type
        )

        for carriage_data in carriages:
            carriage_num = carriage_data.get("carriage_num")
            total_num = carriage_data.get("total_num")
            price = carriage_data.get("price")

            Carriage.objects.create(
                carriage_num=carriage_num,
                total_num=total_num,
                price=price,
                train=train
            )

        for stop_data in stops:
            station_name = stop_data.get("station_name")
            arrival_time = stop_data.get("arrival_time")
            duration = stop_data.get("duration")
            sequence = stop_data.get("sequence")

            # 获取对应的站点对象
            station = Station.objects.get(name=station_name)
            Stop.objects.create(
                train=train,
                station=station,
                arrival_time=arrival_time,
                duration=duration,
                sequence=sequence
            )

        message = '列车添加成功'
        return Response({'message': message}, status=status.HTTP_201_CREATED)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_ticket(request):
    try:
        identity = request.session.get('identity', None)
        if identity != 'system_admin':
            message = '无效权限'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data

        start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%d")
        end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%d")
        train_name = data.get('train_name')

        train = Train.objects.get(name=train_name)
        carriages = train.carriage_set.all()

        current_date = start_date
        while current_date <= end_date:
            for carriage in carriages:
                Ticket.objects.create(
                    date=datetime.combine(current_date, datetime.min.time()),
                    train=train,
                    carriage=carriage,
                    remaining_count=carriage.total_num
                )
            current_date += timedelta(days=1)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def get_train_list(request):
    try:
        identity = request.session.get('identity', None)
        if identity != 'system_admin':
            message = '无效权限'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        trains = Train.objects.all()
        train_data = []
        for train in trains:
            stops = train.stop_set.all()
            carriages = train.carriage_set.all()

            stop_data = []
            for stop in sorted(stops, key=lambda x: x.sequence):
                stop_data.append({
                    'sequence': stop.sequence,
                    'station_name': stop.station.name,
                    'arrival_time': stop.arrival_time,
                    'duration': stop.duration
                })

            carriage_data = []
            for carriage in sorted(carriages, key=lambda x: x.carriage_num):
                carriage_data.append({
                    'carriage_num': carriage.carriage_num,
                    'type': carriage.type,
                    'total_num': carriage.total_num,
                    'price': carriage.price
                })

            train_data.append({
                'train_name': train.name,
                'train_type': train.train_type,
                'stops': stop_data,
                'carriages': carriage_data
            })
        message = '获取列车列表信息成功'
        return Response({'message': message, 'data': train_data}, status=status.HTTP_200_OK)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def remove_train(request):
    try:
        identity = request.session.get('identity', None)
        if identity != 'system_admin':
            message = '无效权限'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        train_name = request.data.get('train_name')

        try:
            train = Train.objects.get(name=train_name)
        except Train.DoesNotExist:
            message = '列车不存在'
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)

        train.delete()

        message = '列车删除成功'
        return Response({'message': message}, status=status.HTTP_200_OK)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def update_train(request):
    try:
        pass
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def query_train(request):
    try:
        data = request.data
        departure_city = data.get('departure_city')
        arrival_city = data.get('arrival_city')
        date = data.get('date')

        start_stops = Stop.objects.filter(station__city=departure_city)
        end_stops = Stop.objects.filter(station__city=arrival_city)

        trains = []
        for start_stop in start_stops:
            for end_stop in end_stops:
                if start_stop.train == end_stop.train and start_stop.sequence < end_stop.sequence:
                    trains.append(start_stop.train)

        train_data = []
        for train in trains:
            carriage_data = {}
            carriages = train.carriage_set.all()
            total_duration = 0

            for carriage in carriages:
                ticket = carriage.ticket_set.filter(date=date).first()
                if carriage.type not in carriage_data:
                    carriage_data[carriage.type] = {
                        'type': carriage.type,
                        'price': carriage.price,
                        'count': 0
                    }
                carriage_data[carriage.type]['count'] += ticket.remaining_count

            start_stop = start_stops.filter(train=train).first()
            end_stop = end_stops.filter(train=train).first()
            if start_stop and end_stop:
                if end_stop.arrival_time >= start_stop.departure_time:
                    total_duration = end_stop.arrival_time - start_stop.departure_time
                else:
                    # 处理跨天情况
                    next_day = timedelta(days=1)
                    total_duration = (end_stop.arrival_time + next_day) - start_stop.departure_time

            train_data.append({
                'train_name': train.name,
                'train_type': train.train_type,
                'total_duration': total_duration,
                'ticket': carriage_data
            })

        message = '查询列车信息成功'
        return Response({'message': message, 'data': train_data}, status=status.HTTP_200_OK)

    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_order(request):
    try:
        pass
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def pay_order(request):
    try:
        pass
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def get_order_list(request):
    try:
        pass
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def return_order(request):
    try:
        pass
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def rebook(request):
    try:
        pass
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

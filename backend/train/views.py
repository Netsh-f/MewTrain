from datetime import datetime, timedelta

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from user.models import User, Passenger
from .models import Station, Train, Carriage, Stop, Ticket, Order, Seat, PassengerOrder


@api_view(['POST'])
def add_station(request):
    try:
        # 检查用户身份
        identity = request.session.get('identity', None)
        if identity != 'railway_admin':
            message = '无效权限'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        # 获取请求体中的数据
        data = request.data
        station_name = data['station_name']
        city = data['city']

        # 创建车站
        station = Station(name=station_name, city=city)
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
        if identity != 'railway_admin':
            message = '无效权限'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data

        train_name = data.get("train_name", None)
        train_type = data.get("train_type", None)
        carriages = data.get("carriages", None)  # 应该传来一个列表，列表内元素看下面
        stops = data.get("stops", None)  # 应该是一个列表

        train = Train.objects.create(
            name=train_name,
            train_type=train_type
        )

        for carriage_data in carriages:  # 遍历列表
            carriage_num = carriage_data.get("carriage_num", None)
            total_num = carriage_data.get("total_num", None)
            # 请确保total_num是一行座位数的整倍数，例如一等座一行3座，total_num需要是3的倍数，一等座4的倍数，二等座5，硬卧3，软卧2，硬座不强制要求，但应该是5的倍数
            price = carriage_data.get("price", None)
            carriage_type = carriage_data.get("carriage_type", None)

            Carriage.objects.create(
                carriage_num=carriage_num,
                type=carriage_type,
                total_num=total_num,
                price=price,
                train=train
            )

        for stop_data in stops:  # 遍历列表
            station_name = stop_data.get("station_name", None)
            arrival_time = stop_data.get("arrival_time", None)
            duration_str = stop_data.get("duration", None)
            sequence = stop_data.get("sequence", None)
            value = int(duration_str)
            duration = timedelta(minutes=value)
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
        if identity != 'railway_admin':
            message = '无效权限'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data

        start_date = datetime.strptime(data.get('start_date', None), "%Y-%m-%d")
        end_date = datetime.strptime(data.get('end_date', None), "%Y-%m-%d")  # 包含开始日期和结束日期，它们可以是同一天，将创建两个日期中间所有日期的票
        train_name = data.get('train_name', None)
        train = Train.objects.get(name=train_name)
        # 重复判断
        if Ticket.objects.filter(train=train):
            message = '不可重复添加'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        carriages = train.carriage_set.all()

        current_date = start_date
        while current_date <= end_date:
            for carriage in carriages:
                ticket = Ticket.objects.create(
                    date=datetime.combine(current_date, datetime.min.time()),
                    train=train,
                    carriage=carriage,
                    remaining_count=carriage.total_num
                )
                max_rows = 0  # 总行数，这里就要求上面add_train的时候total_num是某个数的整数倍
                seat_locations = []  # 位置的名称，硬座此项为空
                if carriage.type == 'BUS':  # 为创建Seat做准备，分六种车型
                    max_rows = carriage.total_num // 3
                    seat_locations = ['A', 'B', 'C']
                elif carriage.type == 'FST':
                    max_rows = carriage.total_num // 4
                    seat_locations = ['A', 'B', 'C', 'D']
                elif carriage.type == 'SND':
                    max_rows = carriage.total_num // 5
                    seat_locations = ['A', 'B', 'C', 'D', 'F']
                elif carriage.type == 'HAW':
                    max_rows = carriage.total_num // 3
                    seat_locations = ['下', '中', '上']
                elif carriage.type == 'SOF':
                    max_rows = carriage.total_num // 2
                    seat_locations = ['下', '上']
                elif carriage.type == 'HAZ':
                    max_rows = carriage.total_num
                    seat_locations = ['']  # 硬座只有编号，故此项为空，但为了下面的循环结构，给了一个空字符串。应该能循环一次吧，请测试
                for num in range(1, max_rows + 1):
                    for location in seat_locations:
                        Seat.objects.create(
                            ticket=ticket,
                            seat_num=num,
                            seat_location=location,
                            is_available=True
                        )
            current_date += timedelta(days=1)
        message = '车票添加成功'
        return Response({'message': message}, status=status.HTTP_201_CREATED)

    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def get_train_list(request):
    try:
        identity = request.session.get('identity', None)
        if identity != 'railway_admin':
            message = '无效权限'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        trains = Train.objects.all()
        train_data = []
        for train in trains:
            stops = train.stop_set.all()
            carriages = train.carriage_set.all()

            stop_data = []  # 将返回一个列表
            for stop in sorted(stops, key=lambda x: x.sequence):
                duration_seconds = stop.duration.total_seconds()
                minutes = int(duration_seconds // 60)
                arrival_time = stop.arrival_time.strftime('%H:%M')

                stop_data.append({
                    'sequence': stop.sequence,
                    'station_name': stop.station.name,
                    'arrival_time': arrival_time,
                    'duration': minutes
                })

            carriage_data = []  # 将返回一个列表
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
                'stops': stop_data,  # 列表
                'carriages': carriage_data  # 列表
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
        if identity != 'railway_admin':
            message = '无效权限'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        train_name = request.data.get('train_name', None)

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
def query_train(request):
    try:
        data = request.data
        departure_city = data.get('departure_city', None)
        arrival_city = data.get('arrival_city', None)
        date_str = data.get('date', None)

        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        start_stops = Stop.objects.filter(station__city=departure_city)
        end_stops = Stop.objects.filter(station__city=arrival_city)

        trains = []  # 双重循环查找相同的车次，找到多个对的stop，效率未测试
        for start_stop in start_stops:
            for end_stop in end_stops:
                if start_stop.train == end_stop.train and start_stop.sequence < end_stop.sequence:
                    trains.append(start_stop.train)
                    break

        train_data = []  # 将返回一个列表
        for train in trains:
            carriage_data = {}  # 这个不是列表但类似列表，每个元素名为车厢(座位)的类型，其每个类型的内容格式相同
            carriages = train.carriage_set.all()
            total_duration = 0
            for carriage in carriages:
                ticket = carriage.ticket_set.filter(date=date).first()
                if ticket is None:
                    message = '存在未设置车票的车厢'
                    return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
                if carriage.type not in carriage_data:
                    carriage_data[carriage.type] = {
                        'price': carriage.price,
                        'count': 0
                    }
                carriage_data[carriage.type]['count'] += ticket.remaining_count  # 累加每种座的剩余数

            start_stop = start_stops.filter(train=train).first()
            end_stop = end_stops.filter(train=train).first()
            is_next_day = False
            if start_stop and end_stop:
                if end_stop.arrival_time >= start_stop.arrival_time:
                    total_duration = datetime.combine(date, end_stop.arrival_time) - datetime.combine(date,
                                                                                                      start_stop.arrival_time)
                else:
                    # 处理跨天情况，默认一列车总时长不会超过24小时
                    is_next_day = True
                    next_day = timedelta(days=1)
                    total_duration = datetime.combine(date + next_day, end_stop.arrival_time) - datetime.combine(date,
                                                                                                                 start_stop.arrival_time)

            total_duration_seconds = total_duration.total_seconds()
            hours = int(total_duration_seconds // 3600)
            minutes = int((total_duration_seconds % 3600) // 60)
            if minutes == 0:
                duration_string = f"{hours}时整"
            else:
                duration_string = f"{hours}时{minutes}分"

            departure_time = start_stop.arrival_time.strftime('%H:%M')
            arrival_time = end_stop.arrival_time.strftime('%H:%M')

            train_data.append({
                'train_name': train.name,
                'train_type': train.train_type,
                'departure_station_name': start_stop.station.name,
                'departure_time': departure_time,
                'arrival_station_name': end_stop.station.name,
                'arrival_time': arrival_time,
                'is_next_day': is_next_day,  # 是否跨天
                'total_duration': duration_string,
                'ticket': carriage_data,
                'start_stop_id': start_stop.id,  # create_order中会用到
                'end_stop_id': end_stop.id  # create_order中会用到
            })

        message = '查询列车信息成功'
        return Response({'message': message, 'data': train_data}, status=status.HTTP_200_OK)

    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def create_order_function(user_id, data):
    user = User.objects.get(id=user_id)

    train_name = data.get('train_name', None)
    carriage_type = data.get('carriage_type', None)
    date = data.get('date', None)
    start_stop_id = data.get('start_stop_id', None)
    end_stop_id = data.get('end_stop_id', None)
    passenger_ids = data.get('passenger_ids', None)

    passengers = Passenger.objects.filter(id__in=passenger_ids)  # 查找得到一个集合
    start_stop = Stop.objects.get(id=start_stop_id)
    end_stop = Stop.objects.get(id=end_stop_id)
    train = Train.objects.get(name=train_name)
    carriages = train.carriage_set.filter(type=carriage_type)  # 一个集合

    if not passengers.exists():
        message = '未找到乘车人信息'
        return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.create(  # 先创建，方便下面passenger_order添加外键
        user=user,
        train=train,
        start_stop=start_stop,
        end_stop=end_stop,
        create_time=datetime.now(),
        order_status='UPD',
    )

    total_price = 0
    for passenger in passengers:
        available_carriage = None
        ticket = None
        for carriage in carriages:
            ticket = carriage.ticket_set.filter(date=date).first()
            if ticket.remaining_count > 0:
                available_carriage = carriage
                break
            if not ticket or not available_carriage:
                message = '无可用座位'
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        if passenger.ticket_type in ['CHI', 'DOM'] or (  # 分情况进行优惠，学生如果购买普通列车是5折，购买高铁是7.5折。这里没有考虑学生一年只能买4张等限制
                passenger.ticket_type == 'STU' and train.train_type == 'REG'):
            price = available_carriage.price * 0.5
        elif passenger.ticket_type == 'STU' and train.train_type == 'HSR':
            price = available_carriage.price * 0.75
        else:
            price = available_carriage.price

        seat = ticket.seat_set.filter(is_available=True).first()
        seat.is_available = False  # 更新座位状态
        ticket.remaining_count -= 1  # 更新剩余座位信息
        total_price += price
        PassengerOrder.objects.create(  # 储存一个订单下，每个乘车人的订单信息，一个订单可能包含不止一位乘车人
            order=order,
            passenger=passenger,
            seat=seat,
            price=price,
        )

    order.total_price = total_price
    order.save()
    return order


@api_view(['POST'])
def create_order(request):
    try:
        identity = request.session.get('identity', None)
        if identity != 'user':
            message = '用户未登录'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.session.get('user_id')

        create_order_function(user_id, request.data)  # 下面要复用，所以写成了函数

        message = '订单创建成功'
        return Response({'message': message}, status=status.HTTP_201_CREATED)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def get_order_list(request):
    try:
        identity = request.session.get('identity', None)
        if identity != 'user':
            message = '用户未登录'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        orders = user.order_set.all()
        order_data = []  # 将返回一个列表
        for order in orders:
            passenger_orders = order.passengerorder_set.all()
            passenger_order_data = []  # 列表里的列表
            for passenger_order in passenger_orders:
                passenger = passenger_order.passenger
                seat = passenger_order.seat
                passenger_order_data.append({
                    'passenger_name': passenger.name,
                    'passenger_id_type': passenger.id_type,
                    'ticket_type': passenger.ticket_type,
                    'carriage_num': seat.ticket.carriage.carriage_num,
                    'seat_num': seat.seat_num,
                    'seat_location': seat.seat_location,
                    'price': passenger_order.price
                })
            if datetime.now() > order.end_stop.arrival_time:  # 更新订单状态，判断是否为过期订单
                order.order_status = 'EXP'
            order_data.append({
                'order_id': order.id,
                'train_name': order.train.name,
                'departure_station_name': order.start_stop.station.name,
                'departure_time': order.start_stop.arrival_time,
                'arrival_station_name': order.end_stop.station.name,
                'arrival_time': order.end_stop.arrival_time,
                'total_price': order.total_price,
                'order_statis': order.order_status,
                'passenger_order_data': passenger_order_data  # 列表
            })
        message = '获取订单列表成功'
        return Response({'message': message, 'data': order_data}, status=status.HTTP_200_OK)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def pay_order(request):
    try:
        identity = request.session.get('identity', None)
        if identity != 'user':
            message = '用户未登录'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        data = request.data
        order_id = data.get('order_id', None)
        order = user.order_set.filter(id=order_id).first()

        if not order:
            message = '订单未找到'
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)
        if order.order_status != 'UPD':
            message = '非未支付订单'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        if user.balance < order.total_price:
            message = '余额不足请充值'
            return Response({'message': message}, status=status.HTTP_402_PAYMENT_REQUIRED)

        user.balance -= order.total_price
        order.order_status = 'PAD'
        message = '支付成功'
        return Response({'message': message}, status=status.HTTP_200_OK)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def return_order(request):
    try:
        identity = request.session.get('identity', None)
        if identity != 'user':
            message = '用户未登录'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        data = request.data
        order_id = data.get('order_id', None)
        order = user.order_set.filter(id=order_id).first()

        if datetime.now() > order.start_stop.arrival_time - timedelta(hours=1):  # 如果距离发车时间小于1小时，或者已经过了发车时间则不能取消订单
            message = '超过了取消订单的时间'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        passenger_orders = order.passengerorder_set
        for passenger_order in passenger_orders:
            seat = passenger_order.seat
            seat.is_available = True  # 更新座位状态
            seat.ticket.remaining_count += 1  # 更新剩余座位信息

        if order.order_status == 'PAD':  # 如果是已支付的状态就退钱
            user.balance += order.total_price

        order.delete()
        message = '取消订单成功'
        return Response({'message': message}, status=status.HTTP_200_OK)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def rebook(request):
    try:
        identity = request.session.get('identity', None)
        if identity != 'user':
            message = '用户未登录'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)

        data = request.data
        original_order_id = request.data.get('original_order_id', None)  # 相比create_order视图，多了这一项
        original_order = user.order_set.filter(id=original_order_id).first()

        if not original_order:
            message = '未找到原始订单'
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)

        if original_order.order_status != 'PAD':
            message = '订单未支付不可改签'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        start_stop = Stop.objects.get(id=data.get('start_stop_id'))
        if original_order.start_stop.station.city != start_stop.station.city:
            message = '出发地与原订单不相同'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        order = create_order_function(user_id, data)  # 这里复用了

        return_price = 0
        passenger_ids = data.get('passenger_ids')
        passenger_orders = original_order.passengerorder_set.filter(id__in=passenger_ids)
        for passenger_order in passenger_orders:
            passenger_order.is_rebooked = True
            return_price += passenger_order.price
        div_price = order.total_price - return_price
        if user.balance < div_price:  # 如果余额不足
            order.delete()
            message = '余额不足'
            return Response({'message': message}, status=status.HTTP_402_PAYMENT_REQUIRED)

        message = '改签成功'
        return Response({'message': message}, status=status.HTTP_200_OK)
    except Exception as e:
        message = '发生错误：{}'.format(str(e))
        return Response({'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_info(request):
    data = {
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
    return Response({'message': message, 'data': data}, status=status.HTTP_200_OK)

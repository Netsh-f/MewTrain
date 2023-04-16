from django.http import JsonResponse
from django.shortcuts import render


def register(request):
    return JsonResponse({'result': 200, 'msg': '连接成功'})

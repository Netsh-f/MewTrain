from django.http import JsonResponse, HttpResponse
from django.views import View


def register(request):
    return JsonResponse({'result': 200, 'msg': '连接成功'})


class LoginView(View):
    def post(self, request, *args, **kwargs):
        return HttpResponse('Hello, POST request')

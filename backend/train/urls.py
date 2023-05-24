from django.urls import path

from train import views

app_name = 'train'

urlpatterns = [
    path('add_station/', views.add_station, name='add_station'),
    path('add_train/', views.add_train, name='add_train'),
    path('get_info/', views.get_info, name='get_info'),
    path('test_send_email/', views.test_send_email),
]

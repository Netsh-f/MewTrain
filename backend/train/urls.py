from django.urls import path

from train import views

app_name = 'train'

urlpatterns = [
    path('add_station/', views.add_station, name='add_station'),
    path('add_train/', views.add_train, name='add_train'),
    path('get_info/', views.get_info, name='get_info'),
    path('add_ticket/', views.add_ticket, name='add_ticket'),
    path('get_train_list/', views.get_train_list, name='get_train_list'),
    path('remove_train/', views.remove_train, name='remove_train'),
    path('query_train/', views.query_train, name='query_train'),
    path('create_order_function/', views.create_order_function, name='create_order_function'),
    path('create_order/', views.create_order, name='create_order'),
    path('get_order_list/', views.get_order_list, name='get_order_list'),
    path('pay_order/', views.pay_order, name='pay_order'),
    path('return_order/', views.return_order, name='return_order'),
    path('rebook/', views.rebook, name='rebook'),
    path('test_send_email/', views.test_send_email),
]

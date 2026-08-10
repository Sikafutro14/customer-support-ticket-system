from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_create, name='ticket_create'),
    path('success/', views.ticket_success, name='ticket_success'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path(
        'tickets/<int:ticket_id>/',
        views.ticket_detail,
        name='ticket_detail'
    ),
]
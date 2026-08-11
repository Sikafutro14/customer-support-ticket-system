from django.urls import path
from . import views



urlpatterns = [
    path('', views.ticket_create, name='ticket_create'),
    path('success/', views.ticket_success, name='ticket_success'),
    path("access-denied/", views.access_denied, name="access_denied"),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path(
        'tickets/<int:ticket_id>/',
        views.ticket_detail,
        name='ticket_detail'
    ),

    path("api/tickets/", views.api_ticket_list, name="api_ticket_list"),

    path(
    "api/tickets/<int:ticket_id>/",
    views.api_ticket_detail,
    name="api_ticket_detail"
),
]
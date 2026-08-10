from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
        "customer_name",
        "category",
        "priority",
        "status",
        "assigned_agent",
        "created_at",
    )

    list_filter = (
        "category",
        "priority",
        "status",
        "created_at",
    )

    search_fields = (
        "subject",
        "customer_name",
        "customer_email",
        "description",
    )

    ordering = ("-created_at",)
from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "customer_name",
            "customer_email",
            "subject",
            "description",
            "category",
            "priority",
            "status",
            "assigned_agent",
            "agent_reply",
            "resolution",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
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

    def validate_customer_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Customer name must contain at least 2 characters."
            )

        return value

    def validate_subject(self, value):
        value = value.strip()

        if len(value) < 5:
            raise serializers.ValidationError(
                "Subject must contain at least 5 characters."
            )

        return value

    def validate_description(self, value):
        value = value.strip()

        if len(value) < 10:
            raise serializers.ValidationError(
                "Description must contain at least 10 characters."
            )

        return value
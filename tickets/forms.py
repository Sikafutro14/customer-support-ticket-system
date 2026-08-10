from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "customer_name",
            "customer_email",
            "subject",
            "description",
            "category",
            "priority",
        ]
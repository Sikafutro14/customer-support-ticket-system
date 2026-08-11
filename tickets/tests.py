from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Ticket


class TicketAPITests(APITestCase):

    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staffuser",
            password="TestPass123!"
        )
        self.staff_user.is_staff = True
        self.staff_user.save()

        self.normal_user = User.objects.create_user(
            username="normaluser",
            password="TestPass123!"
        )

        self.ticket = Ticket.objects.create(
            customer_name="Test Customer",
            customer_email="test@example.com",
            subject="Internet problem",
            description="The internet connection is not working.",
            category="technical",
            priority="urgent",
            status="open",
        )

        self.list_url = reverse("api_ticket_list")

        self.detail_url = reverse(
            "api_ticket_detail",
            args=[self.ticket.id]
        )

    def test_staff_can_view_ticket_list(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_non_staff_cannot_view_ticket_list(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_public_user_can_create_ticket(self):
        data = {
            "customer_name": "New Customer",
            "customer_email": "new@example.com",
            "subject": "Payment problem",
            "description": "I cannot complete my payment.",
            "category": "billing",
            "priority": "medium",
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Ticket.objects.count(),
            2
        )

    def test_staff_can_view_single_ticket(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["subject"],
            "Internet problem"
        )

    def test_staff_can_patch_ticket(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.patch(
            self.detail_url,
            {
                "status": "resolved"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.ticket.refresh_from_db()

        self.assertEqual(
            self.ticket.status,
            "resolved"
        )

    def test_search_filters_tickets(self):
        self.client.force_authenticate(user=self.staff_user)

        Ticket.objects.create(
            customer_name="Another Customer",
            customer_email="another@example.com",
            subject="Payment failure",
            description="Payment is failing.",
            category="billing",
            priority="medium",
            status="open",
        )

        response = self.client.get(
            self.list_url,
            {
                "search": "Internet"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]["subject"],
            "Internet problem"
        )

    def test_status_filter(self):
        self.client.force_authenticate(user=self.staff_user)

        Ticket.objects.create(
            customer_name="Resolved Customer",
            customer_email="resolved@example.com",
            subject="Resolved issue",
            description="This issue is resolved.",
            category="technical",
            priority="low",
            status="resolved",
        )

        response = self.client.get(
            self.list_url,
            {
                "status": "resolved"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]["status"],
            "resolved"
        )

    def test_priority_filter(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.get(
            self.list_url,
            {
                "priority": "urgent"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]["priority"],
            "urgent"
        )
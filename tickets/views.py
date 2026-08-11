from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .forms import TicketForm, TicketUpdateForm
from .models import Ticket
from .serializers import TicketSerializer


@api_view(["GET"])
@permission_classes([IsAdminUser])
def api_ticket_list(request):
    tickets = Ticket.objects.all().order_by("-created_at")

    serializer = TicketSerializer(
        tickets,
        many=True
    )

    return Response(serializer.data)


def is_support_agent(user):
    return user.is_authenticated and user.is_staff


def access_denied(request):
    return render(
        request,
        "tickets/access_denied.html"
    )


def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("ticket_success")

    else:
        form = TicketForm()

    return render(
        request,
        "tickets/ticket_form.html",
        {"form": form}
    )


def ticket_success(request):
    return render(
        request,
        "tickets/ticket_success.html"
    )


@user_passes_test(
    is_support_agent,
    login_url="/access-denied/"
)
def ticket_list(request):
    tickets = Ticket.objects.all().order_by("-created_at")

    # Dashboard statistics
    total_tickets = tickets.count()
    open_tickets = tickets.filter(status="open").count()
    in_progress_tickets = tickets.filter(status="in_progress").count()
    resolved_tickets = tickets.filter(status="resolved").count()

    # Search and filter values
    search = request.GET.get("search", "")
    status = request.GET.get("status", "")
    priority = request.GET.get("priority", "")

    # Search by subject
    if search:
        tickets = tickets.filter(
            subject__icontains=search
        )

    # Filter by status
    if status:
        tickets = tickets.filter(
            status=status
        )

    # Filter by priority
    if priority:
        tickets = tickets.filter(
            priority=priority
        )

    context = {
        "tickets": tickets,
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress_tickets,
        "resolved_tickets": resolved_tickets,
        "search": search,
        "selected_status": status,
        "selected_priority": priority,
    }

    return render(
        request,
        "tickets/ticket_list.html",
        context
    )


@user_passes_test(
    is_support_agent,
    login_url="/access-denied/"
)
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )

    if request.method == "POST":
        form = TicketUpdateForm(
            request.POST,
            instance=ticket
        )

        if form.is_valid():
            form.save()

            return redirect(
                "ticket_detail",
                ticket_id=ticket.id
            )

    else:
        form = TicketUpdateForm(
            instance=ticket
        )

    return render(
        request,
        "tickets/ticket_detail.html",
        {
            "ticket": ticket,
            "form": form,
        }
    )

    @api_view(["GET"])
    @permission_classes([IsAdminUser])
    def api_ticket_list(request):
      tickets = Ticket.objects.all().order_by("-created_at")

    serializer = TicketSerializer(
        tickets,
        many=True
    )

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def api_ticket_detail(request, ticket_id):
    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )

    serializer = TicketSerializer(ticket)

    return Response(serializer.data)
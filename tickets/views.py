from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import TicketForm, TicketUpdateForm
from .models import Ticket


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


@login_required
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
        tickets = tickets.filter(subject__icontains=search)

    # Filter by status
    if status:
        tickets = tickets.filter(status=status)

    # Filter by priority
    if priority:
        tickets = tickets.filter(priority=priority)

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


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        form = TicketUpdateForm(request.POST, instance=ticket)

        if form.is_valid():
            form.save()
            return redirect("ticket_detail", ticket_id=ticket.id)

    else:
        form = TicketUpdateForm(instance=ticket)

    return render(
        request,
        "tickets/ticket_detail.html",
        {
            "ticket": ticket,
            "form": form,
        }
    )
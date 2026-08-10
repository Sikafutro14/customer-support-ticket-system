from django.shortcuts import render, redirect
from .forms import TicketForm
from .models import Ticket


def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("ticket_success")
    else:
        form = TicketForm()

    return render(request, "tickets/ticket_form.html", {"form": form})


def ticket_success(request):
    return render(request, "tickets/ticket_success.html")


def ticket_list(request):
    tickets = Ticket.objects.all().order_by("-created_at")

    return render(
        request,
        "tickets/ticket_list.html",
        {"tickets": tickets},
    )
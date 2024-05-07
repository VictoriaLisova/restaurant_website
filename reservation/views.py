from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from .models import Reservation
from .forms import ReserveTableForm


def reserve_table(request):
    form = ReserveTableForm()

    if request.method == 'POST':
        form = ReserveTableForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Резервація пройшла успішно!')

    context = {'form': form}
    return render(request, 'Reservation/reservation.html', context)

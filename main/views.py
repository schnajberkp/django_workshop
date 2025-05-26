from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Room, Booking
from datetime import datetime, date
from django.utils.timezone import now

# Create your views here.

def room_list(request):
    rooms = Room.objects.all()
    today = date.today()

    for room in rooms:
        room.booked_today = room.booking_set.filter(date=today).exists()

    return render(request, 'main/room_list.html', {'rooms': rooms})

def room_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        capacity = request.POST.get('capacity', '').strip()
        projector = bool(request.POST.get('projector'))

        errors = []

        # Validate name
        if not name:
            errors.append("Room name is required.")
        elif Room.objects.filter(name=name).exists():
            errors.append("Room with this name already exists.")
        # Validate capacity
        if not capacity.isdigit() or int(capacity) <= 0:
            errors.append("Capacity must be a positive integer.")
        if errors:
            return render(request, 'main/room_add.html', {
                'errors': errors,
                'name': name,
                'capacity': capacity,
                'projector': projector
            })
        # Create the room
        Room.objects.create(
            name=name,
            capacity=int(capacity),
            projector=projector
        )
        return redirect('room_list')
    return render(request, 'main/room_add.html')

def room_delete(request, id):
    room = get_object_or_404(Room, id=id)
    room.delete()
    return redirect('room_list')

def room_edit(request, id):
    room = get_object_or_404(Room, id=id)

    if request.method =='POST':
        name = request.POST.get('name', '').strip()
        capacity = request.POST.get('capacity', '').strip()
        projector = bool(request.POST.get('projector'))

        errors = []

        # Validate name
        if not name:
            errors.append("Room name cannot be empty.")
        elif Room.objects.exclude(id=room.id).filter(name__iexact=name).exists():
            errors.append("Room with this name already exists.")

        # Validate capacity
        if not capacity.isdigit() or int(capacity) <= 0:
            errors.append("Capacity must be a positive integer.")

        if errors:
            return render(request, 'main/room_edit.html', {
                'errors': errors,
                'room': room,
                'name': name,
                'capacity': capacity,
                'projector': projector,
            })
        # Update the room
        room.name = name
        room.capacity = int(capacity)
        room.projector = projector
        room.save()

        return redirect('room_list')
    # Get method 
    return render(request, 'main/room_edit.html', {
        'room': room,
        'name': room.name,
        'capacity': room.capacity,
        'projector': room.projector
    })


def room_reserve(request, id):
    room = get_object_or_404(Room, id=id)
    all_bookings = room.booking_set.order_by('date')  

    if request.method == 'POST':
        reservation_date = request.POST.get('date')
        comment = request.POST.get('comment', '').strip()
        errors = []

        if not reservation_date:
            errors.append("Please select a date.")
        else:
            try:
                reservation_date_obj = date.fromisoformat(reservation_date)
                if reservation_date_obj < date.today():
                    errors.append("You cannot reserve a room in the past.")
                elif Booking.objects.filter(room=room, date=reservation_date_obj).exists():
                    errors.append("This room is already booked for the selected date.")
            except ValueError:
                errors.append("Invalid date format.")

        if errors:
            return render(request, 'main/room_reserve.html', {
                'room': room,
                'errors': errors,
                'comment': comment,
                'date': reservation_date,
                'all_bookings': all_bookings,  
            })

        Booking.objects.create(
            room=room,
            date=reservation_date_obj,
            comment=comment
        )

        room.booked = True
        room.save()

        return redirect('room_list')

    return render(request, 'main/room_reserve.html', {
        'room': room,
        'all_bookings': all_bookings  
    })



def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    bookings = room.booking_set.filter(date__gte=date.today()).order_by('date')
    
    return render(request, 'main/room_detail.html', {
        'room': room,
        'bookings': bookings,
    })



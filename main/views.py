from django.shortcuts import render

# Create your views here.

def room_list(request):
    return render(request, 'main/room_list.html')

def room_add(request):
    return render(request, 'main/room_add.html')

from django.contrib import messages
from django.shortcuts import render,redirect
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Room, Device
from django.http import JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


@login_required(login_url='login')
def home(request):
    rooms = Room.objects.all().prefetch_related("device_set")
    return render(request, "home.html", {"rooms": rooms})

@login_required(login_url='login')
def devices(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("deu bom")
            return redirect("home")
        else:
            messages.error(request, "Usuário ou senha incorretos.")
            return redirect("login")

    return render(request, "login.html")
    

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "As senhas não conferem.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Esse email já está cadastrado.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=username
        )

        messages.success(request, "Conta criada com sucesso! Faça login.")
        return redirect("login")

    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect("login")

def create_device(request):
    if request.method == "POST":
        name = request.POST.get("name")
        device_type = request.POST.get("device_type")
        porta = request.POST.get("porta")
        device_id = request.POST.get("device_id")
        device_input = request.POST.get("device_input")
        room_id = request.POST.get("room")

        device_type = True if device_type == "1" else False
        device_input = True if device_input == "1" else False

        room = Room.objects.get(id=room_id)

        # Lógica inicial
        if device_type:  # sensor
            analogico = 0
            digital = False
        else:  # atuador
            analogico = 0
            digital = False

        Device.objects.create(
            device_id=device_id,
            name=name,
            port=porta,
            device_input=device_input,
            device_type=device_type,
            analog_value=analogico,
            digital_value=digital,
            room=room
        )

        messages.success(request, "Dispositivo criado com sucesso!")
        return redirect("home")

    return redirect("home")

def create_room(request):
    if request.method == "POST":
        name = request.POST.get("name")

        Room.objects.create(
            user=request.user,
            name=name
        )

        messages.success(request, "Cômodo criado com sucesso!")
        return redirect("home")

    return redirect("home")

def toggle_device(request, pk):
    device = get_object_or_404(Device, pk=pk)
    device.digital_value= not device.digital_value
    device.save()
    return redirect("home")

def set_analog_value(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)

    if request.method == "POST":
        device.analog_value = int(request.POST.get("value"))
        device.save()

    return redirect("devices_page")  # ajuste para a sua rota


from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import Device
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def read_device(request, device_id):
    """
    Retorna o valor atual do dispositivo (analógico ou digital)
    """
    device = get_object_or_404(Device, device_id=device_id)
    
    if device.device_input:  # Digital
        return Response({
            "device_id": device.device_id,
            "type": "digital",
            "value": device.digital_value
        })
    else:  # Analógico
        return Response({
            "device_id": device.device_id,
            "type": "analog",
            "value": device.analog_value
        })


@api_view(['POST'])
def write_device(request, device_id):
    """
    Atualiza o valor do dispositivo (analógico ou digital)
    Espera JSON: { "value": 123 } para analógico ou { "value": true/false } para digital
    """
    device = get_object_or_404(Device, device_id=device_id)
    data = request.data

    if 'value' not in data:
        return Response({"error": "Campo 'value' obrigatório"}, status=400)

    if device.device_input:  # Digital
        device.digital_value = bool(data['value'])
    else:  # Analógico
        device.analog_value = int(data['value'])
        if device.analog_value < 0: device.analog_value = 0
        if device.analog_value > 255: device.analog_value = 255

    device.save()
    return Response({"success": True})

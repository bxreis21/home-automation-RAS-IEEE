from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("devices/create/", views.create_device, name="device_create"),
    path("rooms/create/", views.create_room, name="create_room"),
    path("devices/toggle/<int:pk>/", views.toggle_device, name="toggle_device"),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path("devices/<int:device_id>/analog/", views.set_analog_value, name="set_analog_value"),
    path('device/<int:device_id>/read/', views.read_device, name='read_device'),
    path('device/<int:device_id>/write/', views.write_device, name='write_device'),
]

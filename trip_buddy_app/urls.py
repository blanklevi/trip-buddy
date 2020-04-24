from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('loggedin', views.log_in),
    path('dashboard', views.success_log_in),
    path('trips/new', views.new_trip_page),
    path('createtrip', views.create_trip),
    path('remove/<int:trip_id>', views.remove_trip),
    path('trips/edit/<int:trip_id>', views.edit_trip_page),
    path('edit/<int:trip_id>', views.edit_trip),
    path('trips/<int:trip_id>', views.trip_page),
    path('trips/join/<int:trip_id>', views.join),
    path('cancel/<int:trip_id>', views.cancel),
    path('logout', views.log_out),
]

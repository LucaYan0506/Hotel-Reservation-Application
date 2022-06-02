from django.urls import path
from . import views

urlpatterns = [
    path('',views.indexView, name="index"),
    path('room_types/',views.room_typeView, name="room_types"),
    path('room_types/form/',views.add_room_type, name="add_room_type"),
    path('room_types/info/',views.get_room_type, name="get_root_type"),
    path('room_types/update/',views.update_room_type, name="update_root_type"),
    path('room_types/delete/',views.delete_room_type, name="delete_root_type"),

    path('floor/',views.floorView, name="floor"),
    path('floor/form/',views.add_floor, name="add_floor"),
    path('floor/info/',views.get_floor, name="get_floor"),
    path('floor/update/',views.update_floor, name="update_floor"),
    path('floor/delete/',views.delete_floor, name="delete_floor"),

    path('amenity/',views.amenityView, name="amenity"),
    path('amenity/form/',views.add_amenity, name="add_amenity"),
    path('amenity/info/',views.get_amenity, name="get_amenity"),
    path('amenity/update/',views.update_amenity, name="update_floor"),
    path('amenity/delete/',views.delete_amenity, name="delete_floor"),

    path('room/',views.roomView, name="room"),
    path('room/form/',views.add_room, name="add_room"),
    path('room/info/',views.get_room, name="get_room"),
    path('room/update/',views.update_room, name="update_floor"),
    path('room/delete/',views.delete_room, name="delete_floor"),
]

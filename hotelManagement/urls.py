from django.urls import path
from . import views

urlpatterns = [
    path('',views.indexView, name="index"),
    path('login/',views.loginView, name="login"),
    path('logout/',views.logout_view, name="logout"),

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
    path('amenity/update/',views.update_amenity, name="update_amenity"),
    path('amenity/delete/',views.delete_amenity, name="delete_amenity"),

    path('room/',views.roomView, name="room"),
    path('room/form/',views.add_room, name="add_room"),
    path('room/info/',views.get_room, name="get_room"),
    path('room/update/',views.update_room, name="update_room"),
    path('room/delete/',views.delete_room, name="delete_room"),

    path('employees/',views.employeesView, name="employees"),
    path('employees/form/',views.add_employees, name="add_employees"),
    path('employees/info/',views.get_employees, name="get_employees"),
    path('employees/update/',views.update_employees, name="update_employees"),
    path('employees/delete/',views.delete_employees, name="delete_employees"),

    path('departments/',views.departmentsView, name="departments"),
    path('departments/form/',views.add_departments, name="add_departments"),
    path('departments/info/',views.get_departments, name="get_departments"),
    path('departments/update/',views.update_departments, name="update_departments"),
    path('departments/delete/',views.delete_departments, name="delete_departments"),

    path('positions/',views.positionsView, name="positions"),
    path('positions/form/',views.add_positions, name="add_positions"),
    path('positions/info/',views.get_positions, name="get_positions"),
    path('positions/update/',views.update_positions, name="update_positions"),
    path('positions/delete/',views.delete_positions, name="delete_positions"),
]

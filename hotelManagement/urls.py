from django.urls import path
from . import views

urlpatterns = [
    path('',views.indexView, name="index"),
    path('login/',views.loginView, name="login"),
    path('logout/',views.logout_view, name="logout"),

    path('image/',views.imageView, name="image"),
    path('image/add/',views.add_image, name="add_image"),
    path('image/info/',views.get_image, name="get_image"),
    path('image/delete/',views.delete_image, name="delete_image"),

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
    path('room/housekeeping/',views.room_housekeepingView, name="housekeeping"),
    path('room/housekeeping/form/',views.add_housekeeping, name="add_housekeeping"),
    path('room/housekeeping/info/',views.get_housekeeping, name="get_housekeeping"),
    path('room/housekeeping/update/',views.update_housekeeping, name="update_housekeeping"),
    path('room/housekeeping/delete/',views.delete_housekeeping, name="delete_housekeeping"),

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

    path('housekeepingStatus/',views.housekeepingStatusView, name="housekeepingStatus"),
    path('housekeepingStatus/form/',views.add_housekeepingStatus, name="add_housekeepingStatus"),
    path('housekeepingStatus/info/',views.get_housekeepingStatus, name="get_housekeepingStatus"),
    path('housekeepingStatus/update/',views.update_housekeepingStatus, name="update_housekeepingStatus"),
    path('housekeepingStatus/delete/',views.delete_housekeepingStatus, name="delete_housekeepingStatus"),

    path('hall_types/',views.hall_typeView, name="hall_types"),
    path('hall_types/form/',views.add_hall_type, name="add_hall_types"),
    path('hall_types/info/',views.get_hall_type, name="get_hall_types"),
    path('hall_types/update/',views.update_hall_type, name="update_hall_types"),
    path('hall_types/delete/',views.delete_hall_type, name="delete_hall_types"),

    path('hall/',views.hallView, name="hall"),
    path('hall/form/',views.add_hall, name="add_hall"),
    path('hall/info/',views.get_hall, name="get_hall"),
    path('hall/update/',views.update_hall, name="update_hall"),
    path('hall/delete/',views.delete_hall, name="delete_hall"),
    path('hall/housekeeping/',views.housekeeping_hallView, name="housekeeping_hall"),
    path('hall/housekeeping/form/',views.add_housekeeping_hall, name="add_housekeeping_hall"),
    path('hall/housekeeping/info/',views.get_housekeeping_hall, name="get_housekeeping_hall"),
    path('hall/housekeeping/update/',views.update_housekeeping_hall, name="update_housekeeping_hall"),
    path('hall/housekeeping/delete/',views.delete_housekeeping_hall, name="delete_housekeeping_hall"),

    path('priceManager/',views.priceManagerView, name="priceManager"),
    path('priceManager/info/',views.get_priceManager, name="get_priceManager"),
    path('priceManager/update/',views.update_priceManager, name="update_priceManager"),

    path('services/',views.servicesView, name="services"),
    path('services/form/',views.add_services, name="add_services"),
    path('services/info/',views.get_services, name="get_services"),
    path('services/update/',views.update_services, name="update_services"),
    path('services/delete/',views.delete_services, name="delete_services"),

    path('coupon/',views.couponView, name="coupon"),
    path('coupon/form/',views.add_coupon, name="add_coupon"),
    path('coupon/info/',views.get_coupon, name="get_coupon"),
    path('coupon/update/',views.update_coupon, name="update_coupon"),
    path('coupon/delete/',views.delete_coupon, name="delete_coupon"),
]

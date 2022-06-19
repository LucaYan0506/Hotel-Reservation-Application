from django.core.management.base import BaseCommand
from datetime import datetime
from hotelManagement.models import Employee,Positions
Positions.objects.filter(pk = 0)
class Command(BaseCommand):
    help = 'Generate an admin'

    def handle(self, *args, **kwargs):
        if Positions.objects.filter(pk = 1).exists() == False:
            position = Positions(name="Hotel Worker")
            position.save()
        if Positions.objects.filter(pk = 2).exists() == False:
            position = Positions(name="Admin")
            position.save()       

        employee = Employee(
            title='Mr',
            gender="M",
            first_name='Admin',
            last_name='Admin',
            username='Admin',
            email='',
            password="admin123",
            confirm_password="admin123",
            date_of_birth= datetime(2003,6,5),
            country_calling_code=44,
            phone_number=1234567890,
            position=Positions.objects.get(pk = 2),
            country="GB",
            city="Manchester",
            address="",
            is_staff=True,
            is_superuser=True,
        )

        employee.set_password(employee.password)
        employee.confirm_password=employee.password,

        
        employee.save()
        
        self.stdout.write('Admin account created')

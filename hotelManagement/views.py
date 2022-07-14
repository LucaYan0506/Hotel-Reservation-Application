from distutils.log import error
from django.shortcuts import render, reverse
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from .models import *
import json

# Create your views here.

def indexView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/index.html')
    
    return HttpResponseRedirect(reverse('login'))

def loginView(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "hotelManagement/login.html", {
                "message": "Invalid username and/or password."
            })

    return render(request,'hotelManagement/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))



def room_typeView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/roomType.html',{
            'form': Room_TypeForm(),
        })
    return HttpResponseRedirect(reverse('login'))

def add_room_type(request):
    if request.method == 'POST':
        formset = Room_TypeForm(request.POST,request.FILES)
        if formset.is_valid():
            formset.save()
            return JsonResponse({
            'Result':'Succeed',
            },
            safe=False)

        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)

    
    return HttpResponse('Make sure that you send a post request')

def get_room_type(request):
    if (request.GET.get('pk')):
        room_type = Room_Type.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(room_type.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = Room_Type.objects.all()

    #if user want specific room type
    if request.GET.get('contain'):
        data =  Room_Type.objects.filter(title__icontains=request.GET.get('contain')).all()

    #get from start to end posts
    data2 = []
    index = 1
    for x in data:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    return JsonResponse({
        'total_room_type':data.count(),
        'room_type':[x.serialize() for x in data2]
        },safe=False)

def update_room_type(request):
    if request.method == 'POST':
        data = request.POST
        room_type = Room_Type.objects.get(pk = data['pk'])
        oldImage = room_type.image
        formset = Room_TypeForm(request.POST,request.FILES)
        if formset.is_valid():
            for key in data:
                if key != 'amenities':
                    setattr(room_type, key, data[key])
            if 'image' in request.FILES:
                room_type.image = request.FILES['image']
            else:
                room_type.image = oldImage
            room_type.description = data['description']
            room_type.amenities.clear()
            for x in data.getlist('amenities'):
                room_type.amenities.add(Amenity.objects.get(pk = x))
            room_type.save()
            return JsonResponse({'Result':'Succeed',},safe=False)
                        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)
        
    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def delete_room_type(request):
    Room_Type.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('room_types'))



def floorView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/floor.html',{
            'form': FloorForm(),
        })

    return HttpResponseRedirect(reverse('login'))

def add_floor(request):
    if request.method == 'POST':
        formset = FloorForm(request.POST)
        if formset.is_valid():
            formset.active = "active" in request.POST
            formset.save()
            return JsonResponse({
            'Result':'Succeed',
            },
            safe=False)

        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)

    return HttpResponse('Make sure that you send a post request')

def get_floor(request):
    if (request.GET.get('pk')):
        floor = Floor.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(floor.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = Floor.objects.all()

    #if user want specific room type
    if request.GET.get('contain'):
        data =  Floor.objects.filter(Name__icontains=request.GET.get('contain')).all()

    #get from start to end posts
    data2 = []
    index = 1
    for x in data:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    return JsonResponse({
        'total_floor':data.count(),
        'floor':[x.serialize() for x in data2]
        },safe=False)

def update_floor(request):
    if request.method == 'POST':
        data = request.POST
        formset = FloorForm(request.POST)
        floor = Floor.objects.get(pk = data['pk'])
        formset.is_valid()
        
        errors = formset.errors.as_data()
       
        if (int)(request.POST['number']) == (int)(floor.number) and 'name' not in errors:
            for key in data:
                setattr(floor, key, data[key])
            floor.active = "active" in data
            floor.save()

            return JsonResponse({'Result':'Succeed',},safe=False)

        if 'number' not in errors and (int)(request.POST['number']) != (int)(floor.number) and 'name' not in errors:
            errors = formset.errors.as_json()
        elif 'name' not in errors:
            errors = '{"name": [{"message": "%s"}]}' % (errors['name'][0].messages[0])
        else:
            errors = '{"number": [{"message": "%s"}]}' % (errors['number'][0].messages[0])

        return JsonResponse({
            'Result':'Failed',
            'error': errors,
            },
            safe=False)
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def delete_floor(request):
    Floor.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('floor'))



def amenityView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/amenity.html',{
            'form': AmenityForm(),
        })

    return HttpResponseRedirect(reverse('login'))
    
def add_amenity(request):
    if request.method == 'POST':
        formset = AmenityForm(request.POST, request.FILES)
        if formset.is_valid():
            formset.active = "active" in request.POST
            formset.save()
            return JsonResponse({
            'Result':'Succeed',
            },
            safe=False)

        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)

    return HttpResponse('Make sure that you send a post request')

def get_amenity(request):
    if (request.GET.get('pk')):
        amenity = Amenity.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(amenity.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = Amenity.objects.all()

    #if user want specific room type
    if request.GET.get('contain'):
        data =  Amenity.objects.filter(Name__icontains=request.GET.get('contain')).all()

    #get from start to end posts
    data2 = []
    index = 1
    for x in data:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    return JsonResponse({
        'total_amenity':data.count(),
        'amenity':[x.serialize() for x in data2]
        },safe=False)

def update_amenity(request):
    if request.method == 'POST':
        data = request.POST
        formset = AmenityForm(request.POST)
        amenity = Amenity.objects.get(pk = data['pk'])
        oldImage = amenity.image 
        if formset.is_valid():
            for key in data:
                setattr(amenity, key, data[key])

            if 'image' in request.FILES:
                amenity.image = request.FILES['image']
            else:
                amenity.image = oldImage
            amenity.active = "active" in data
            amenity.save()

            return JsonResponse({'Result':'Succeed',},safe=False)
                        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def delete_amenity(request):
    Amenity.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('amenity'))



def roomView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/room.html',{
            'form': RoomForm(),
        })

    return HttpResponseRedirect(reverse('login'))

def add_room(request):
    if request.method == 'POST':
        formset = RoomForm(request.POST)
        if formset.is_valid():
            formset.save()
            return JsonResponse({
            'Result':'Succeed',
            },
            safe=False)

        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)

    return HttpResponse('Make sure that you send a post request')

def get_room(request):
    if (request.GET.get('pk')):
        room = Room.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(room.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = Room.objects.all()

    #if user want specific room type
    if request.GET.get('contain'):
        data =  Room.objects.filter(room_number__icontains=request.GET.get('contain')).all()

    #get from start to end posts
    data2 = []
    index = 1
    for x in data:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    return JsonResponse({
        'total_room':data.count(),
        'room':[x.serialize() for x in data2]
        },safe=False)

def update_room(request):
    if request.method == 'POST':
        data = request.POST
        formset = RoomForm(request.POST)
        room = Room.objects.get(pk = data['pk'])
                
        errors = formset.errors.as_data()
       
        if (int)(data['room_number']) == (int)(room.room_number) and 'room_type' not in errors and 'floor' not in errors:
            room.room_type = Room_Type.objects.get(pk = data['room_type'])
            room.floor = Floor.objects.get(pk = data['floor'])
            room.room_number = data['room_number']
            room.save()

            return JsonResponse({'Result':'Succeed',},safe=False)
                        
        if (int)(data['room_number']) == (int)(room.room_number):
            errors_copy = errors
            errors = ""
            if 'floor' in errors_copy:
                errors = '{"floor": [{"message": "%s"}]}' % (errors_copy['floor'][0].messages[0])
            if 'room_type' in errors_copy :
                errors = '{"room_type": [{"message": "%s"}]}' % (errors_copy['room_type'][0].messages[0])
        else:
            errors = formset.errors.as_json()
        return JsonResponse({
            'Result':'Failed',
            'error': errors,
            },
            safe=False)
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def delete_room(request):
    Room.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('room'))

def room_housekeepingView(request):
    id = request.GET.get('id') or None
    if request.user.is_authenticated:
        return render(request,'hotelManagement/housekeeping.html',{
            'form': HousekeepingForm(),
            'id':id,
            'employees':Employee.objects.all(),
            'rooms':Room.objects.all(),
            'housekeeping_statuses':HousekeepingStatus.objects.all(),
        })

    return HttpResponseRedirect(reverse('login'))

def get_housekeeping(request):
    if (request.GET.get('pk')):
        housekeeping = Housekeeping.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(housekeeping.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = Housekeeping.objects.all()

    #if user want specific housekeeping
    if request.GET.get('filter') == 'True':
        if request.GET.get('assigned_to'):
            user_query = request.GET.get('assigned_to')
            if user_query[-1] == ',':
                user_query = user_query[:-1]
            list = set(user_query.split(','))
            data = data.filter(assign_to__in = list)
        if request.GET.get('room_number'):
            user_query = request.GET.get('room_number')
            if user_query[-1] == ',':
                user_query = user_query[:-1]
            list = set(user_query.split(','))
            data = data.filter(room__in = list)
        if request.GET.get('housekeeping_status'):
            user_query = request.GET.get('housekeeping_status')
            if user_query[-1] == ',':  
                user_query = user_query[:-1]
            list = set(user_query.split(','))
            data = data.filter(housekeeping_status__in = list)
    #get from start to end posts
    data2 = []
    index = 1
    for x in data:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    return JsonResponse({
        'total_housekeeping':data.count(),
        'housekeeping':[x.serialize() for x in data2]
        },safe=False)

def add_housekeeping(request):
    if request.method == 'POST':
        formset = HousekeepingForm(request.POST)
        if formset.is_valid():
            formset.save()

            return JsonResponse({'Result':'Succeed',},safe=False)
                        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def update_housekeeping(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        formset = HousekeepingForm(request.POST)
        housekeeping = Housekeeping.objects.get(pk = data['pk'])
        if formset.is_valid():
            housekeeping.room = Room.objects.get(pk = data['room'])
            housekeeping.housekeeping_status = HousekeepingStatus.objects.get(pk = data['housekeeping_status'])
            housekeeping.assign_to = Employee.objects.get(pk = data['assign_to'])
            housekeeping.save()

            return JsonResponse({'Result':'Succeed',},safe=False)
                        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def delete_housekeeping(request):
    Housekeeping.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('housekeeping'))


def employeesView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/employees.html',{
            'form': EmployeeForm(),
            'user_permissions':User_permission.objects.all()
        })

    return HttpResponseRedirect(reverse('login'))

def add_employees(request):
    if request.method == 'POST':
        formset = EmployeeForm(request.POST)
        if formset.is_valid():
            formset.save()
            employee = Employee.objects.last()
            for x in list(request.POST['position']):
                employee.user_permission.add(User_permission.objects.get(pk = x))
            employee.save()
            return JsonResponse({
            'Result':'Succeed',
            },
            safe=False)

        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)

    return HttpResponse('Make sure that you send a post request')

def get_employees(request):
    if (request.GET.get('pk')):
        employee = Employee.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(employee.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = Employee.objects.all()

    #if user want specific Employee
    if request.GET.get('contain'):
        data =  Employee.objects.filter(username__icontains=request.GET.get('contain')).all()

    #get from start to end posts
    data2 = []
    index = 1
    for x in data:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    return JsonResponse({
        'total_employees':data.count(),
        'employees':[x.serialize() for x in data2]
        },safe=False)

def update_employees(request):
    if request.method == 'POST':
        data = request.POST
        formset = EmployeeForm(data)
        employee = Employee.objects.get(pk = data['pk'])
        employee.user_permission.clear()
        oldImage = employee.image
        errors = json.loads(formset.errors.as_json())

        if 'password' in errors and 'confirm_password' in errors and 'username' in errors and data['username'] == employee.username and len(errors) == 3:
            for key in data:
                if key == 'password' or key == 'confirm_password':
                    continue
                if key == 'department':
                    employee.department = Departments.objects.get(pk = data[key])
                    continue
                if key == 'position':
                    employee.position = Positions.objects.get(pk = data[key])
                    continue
                if key == 'user_permission':
                    for x in list(data[key]):
                        employee.user_permission.add(User_permission.objects.get(pk = x))
                    continue
                  
                setattr(employee, key, data[key])

            if 'image' in request.FILES:
                employee.image = request.FILES['image']
            else:
                employee.image = oldImage
                
            employee.save()
            return JsonResponse({'Result':'Succeed',},safe=False)

        errors.pop('password')
        errors.pop('confirm_password')

        return JsonResponse({
            'Result':'Failed',
            'error': json.dumps(errors),
            },
            safe=False)
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def delete_employees(request):
    Employee.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('employees'))



def departmentsView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/departments.html',{
            'form': DepartmentsForm(),
        })

    return HttpResponseRedirect(reverse('login'))

def add_departments(request):
    if request.method == 'POST':
        formset = DepartmentsForm(request.POST)
        if formset.is_valid():
            formset.save()
            return JsonResponse({
            'Result':'Succeed',
            },
            safe=False)

        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)

    return HttpResponse('Make sure that you send a post request')

def get_departments(request):
    if (request.GET.get('pk')):
        departments = departments.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(departments.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = Departments.objects.all()

    #if user want specific position
    if request.GET.get('contain'):
        data =  Departments.objects.filter(name__icontains=request.GET.get('contain')).all()

    #get from start to end posts
    data2 = []
    index = 1
    for x in data:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    return JsonResponse({
        'total_departments':data.count(),
        'departments':[x.serialize() for x in data2]
        },safe=False)

def update_departments(request):
    if request.method == 'POST':
        data = request.POST
        formset = DepartmentsForm(data)
        departments = Departments.objects.get(pk = data['pk'])
        if formset.is_valid():
            departments.name = data['name']
            departments.description = data['description']
            departments.save()

            return JsonResponse({'Result':'Succeed',},safe=False)
                        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def delete_departments(request):
    Departments.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('departments'))



def positionsView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/positions.html',{
            'form': PositionsForm(),
        })

    return HttpResponseRedirect(reverse('login'))

def add_positions(request):
    if request.method == 'POST':
        formset = PositionsForm(request.POST)
        if formset.is_valid():
            formset.save()
            return JsonResponse({
            'Result':'Succeed',
            },
            safe=False)

        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)

    return HttpResponse('Make sure that you send a post request')

def get_positions(request):
    if (request.GET.get('pk')):
        positions = Positions.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(positions.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = Positions.objects.all()

    #if user want specific position
    if request.GET.get('contain'):
        data =  Positions.objects.filter(name__icontains=request.GET.get('contain')).all()

    #get from start to end posts
    data2 = []
    index = 1
    for x in data:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    return JsonResponse({
        'total_positions':data.count(),
        'positions':[x.serialize() for x in data2]
        },safe=False)

def update_positions(request):
    if request.method == 'POST':
        data = request.POST
        formset = PositionsForm(data)
        positions = Positions.objects.get(pk = data['pk'])
        if formset.is_valid():
            positions.name = data['name']
            positions.description = data['description']
            positions.save()

            return JsonResponse({'Result':'Succeed',},safe=False)
                        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def delete_positions(request):
    Positions.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('positions'))



def housekeepingStatusView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/housekeepingStatus.html',{
            'form': HousekeepingStatusForm(),
        })

    return HttpResponseRedirect(reverse('login'))

def add_housekeepingStatus(request):
    if request.method == 'POST':
        formset = HousekeepingStatusForm(request.POST)
        if formset.is_valid():
            formset.save()
            return JsonResponse({
            'Result':'Succeed',
            },
            safe=False)

        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)

    return HttpResponse('Make sure that you send a post request')

def get_housekeepingStatus(request):
    if (request.GET.get('pk')):
        housekeeping = HousekeepingStatus.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(housekeeping.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = HousekeepingStatus.objects.all()

    #if user want specific position
    if request.GET.get('contain'):
        data =  HousekeepingStatus.objects.filter(name__icontains=request.GET.get('contain')).all()

    #get from start to end posts
    data2 = []
    index = 1
    for x in data:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    return JsonResponse({
        'total_housekeepingStatus':data.count(),
        'housekeepingStatus':[x.serialize() for x in data2]
        },safe=False)

def update_housekeepingStatus(request):
    if request.method == 'POST':
        data = request.POST
        formset = HousekeepingStatusForm(data)
        housekeeping = HousekeepingStatus.objects.get(pk = data['pk'])
        if formset.is_valid():
            housekeeping.name = data['name']
            housekeeping.description = data['description']
            if 'active' in data:
                print(data['active'])
                housekeeping.active = True
            else:
                print(False)
                housekeeping.active = False 

            housekeeping.save()

            return JsonResponse({'Result':'Succeed',},safe=False)
                        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def delete_housekeepingStatus(request):
    HousekeepingStatus.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('housekeeping'))

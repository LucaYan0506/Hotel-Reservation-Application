from datetime import datetime
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



def imageView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/image.html',{
            'form': ImageForm(),
            'folders': ImageFolder.objects.all()
        })
    return HttpResponseRedirect(reverse('login'))

def add_image(request):
    if request.method == 'POST':
        if request.POST['folder'] == '-1':
            #create new folder
            new_folder = ImageFolder.objects.create(name=request.POST['folder_name'])
            new_folder.save()
            image = Image(folder=new_folder)
            image.image = request.FILES['image']
            image.save()
            return JsonResponse({
            'Result':'Succeed',
            },
            safe=False)
        formset = ImageForm(request.POST,request.FILES)
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

def get_image(request):
    if (request.GET.get('pk')):
        image = Image.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(image.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = Image.objects.all()

    #if user want specific room type
    if request.GET.get('contain'):
        data =  Image.objects.filter(title__icontains=request.GET.get('contain')).all()

    #get from start to end posts
    data2 = []
    index = 1
    for x in data:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    return JsonResponse({
        'total_image':data.count(),
        'image':[x.serialize() for x in data2]
        },safe=False)

def delete_image(request):
    instance = Image.objects.get(pk = request.GET.get('pk'))
    instance.image.delete(save=False)
    instance.delete()

    return HttpResponseRedirect(reverse('image'))




def room_typeView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/roomType.html',{
            'form': Room_TypeForm(),
        })
    return HttpResponseRedirect(reverse('login'))

def add_room_type(request):
    if request.method == 'POST':
        formset = Room_TypeForm(request.POST)
        if formset.is_valid():
            formset.save()
            room_type = Room_Type.objects.last()
            for x in request.POST.getlist('image'):
                room_type.image.add(Image.objects.get(pk = x))
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
        formset = Room_TypeForm(request.POST,request.FILES)

        if formset.is_valid():
            for key in data:
                if key != 'amenities' and key != 'image':
                    setattr(room_type, key, data[key])

            room_type.image.clear()
            for x in data.getlist('image'):
                room_type.image.add(Image.objects.get(pk = x))

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

            amenity = Amenity.objects.last()
            for x in request.POST.getlist('image'):
                amenity.image.add(Image.objects.get(pk = x))

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
        if formset.is_valid():
            for key in data:
                if key != 'image' and key != 'active':
                    setattr(amenity, key, data[key])

            if 'active' in data:
                amenity.active = True
            else:
                amenity.active = False

            amenity.description = data['description']

            amenity.image.clear()
            for x in data.getlist('image'):
                amenity.image.add(Image.objects.get(pk = x))
            
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
            'form': HousekeepingForRoomForm(),
            'id':id,
            'employees':Employee.objects.all(),
            'rooms':Room.objects.all(),
            'housekeeping_statuses':HousekeepingStatus.objects.all(),
        })

    return HttpResponseRedirect(reverse('login'))

def get_housekeeping(request):
    if (request.GET.get('pk')):
        housekeeping = HousekeepingForRoom.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(housekeeping.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = HousekeepingForRoom.objects.all()

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
        formset = HousekeepingForRoomForm(request.POST)
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
        formset = HousekeepingForRoomForm(request.POST)
        housekeeping = HousekeepingForRoom.objects.get(pk = data['pk'])
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
    HousekeepingForRoom.objects.get(pk = request.GET.get('pk')).delete()

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
            employee.set_password(request.POST['password'])
            employee.confirm_password=employee.password,

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
                housekeeping.active = True
            else:
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



def hall_typeView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/hall_type.html',{
            'form': Hall_TypeForm(),
        })
    return HttpResponseRedirect(reverse('login'))

def add_hall_type(request):
    if request.method == 'POST':
        formset = Hall_TypeForm(request.POST)
        if formset.is_valid():
            formset.save()
            hall_type = Hall_Type.objects.last()
            for x in request.POST.getlist('image'):
                hall_type.image.add(Image.objects.get(pk = x))
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

def get_hall_type(request):
    if (request.GET.get('pk')):
        hall_type = Hall_Type.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(hall_type.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = Hall_Type.objects.all()

    #if user want specific room type
    if request.GET.get('contain'):
        data =  Hall_Type.objects.filter(title__icontains=request.GET.get('contain')).all()

    #get from start to end posts
    data2 = []
    index = 1
    for x in data:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    return JsonResponse({
        'total_hall_type':data.count(),
        'hall_type':[x.serialize() for x in data2]
        },safe=False)

def update_hall_type(request):
    if request.method == 'POST':
        data = request.POST
        hall_type = Hall_Type.objects.get(pk = data['pk'])
        formset = Hall_TypeForm(request.POST,request.FILES)

        if formset.is_valid():
            for key in data:
                if key != 'amenities' and key != 'image':
                    setattr(hall_type, key, data[key])

            hall_type.image.clear()
            for x in data.getlist('image'):
                hall_type.image.add(Image.objects.get(pk = x))

            hall_type.description = data['description']

            hall_type.amenities.clear()
            for x in data.getlist('amenities'):
                hall_type.amenities.add(Amenity.objects.get(pk = x))
            hall_type.save()
            return JsonResponse({'Result':'Succeed',},safe=False)
                        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)
        
    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def delete_hall_type(request):
    Hall_Type.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('hall_types'))



def hallView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/hall.html',{
            'form': HallForm(),
        })

    return HttpResponseRedirect(reverse('login'))

def add_hall(request):
    if request.method == 'POST':
        formset = HallForm(request.POST)
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

def get_hall(request):
    if (request.GET.get('pk')):
        room = Hall.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(room.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = Hall.objects.all()

    #if user want specific room type
    if request.GET.get('contain'):
        data =  Hall.objects.filter(hall_number__icontains=request.GET.get('contain')).all()

    #get from start to end posts
    data2 = []
    index = 1
    for x in data:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    return JsonResponse({
        'total_hall':data.count(),
        'hall':[x.serialize() for x in data2]
        },safe=False)

def update_hall(request):
    if request.method == 'POST':
        data = request.POST
        formset = HallForm(request.POST)
        hall = Hall.objects.get(pk = data['pk'])
                
        errors = formset.errors.as_data()
       
        if (int)(data['hall_number']) == (int)(hall.hall_number) and 'hall_type' not in errors and 'floor' not in errors:
            hall.hall_type = Hall_Type.objects.get(pk = data['hall_type'])
            hall.floor = Floor.objects.get(pk = data['floor'])
            hall.hall_number = data['hall_number']
            hall.save()

            return JsonResponse({'Result':'Succeed',},safe=False)
                        
        if (int)(data['hall_number']) == (int)(hall.hall_number):
            errors_copy = errors
            errors = ""
            if 'floor' in errors_copy:
                errors = '{"floor": [{"message": "%s"}]}' % (errors_copy['floor'][0].messages[0])
            if 'hall_type' in errors_copy :
                errors = '{"hall_type": [{"message": "%s"}]}' % (errors_copy['hall_type'][0].messages[0])
        else:
            errors = formset.errors.as_json()

        print(formset.errors.as_json())
        return JsonResponse({
            'Result':'Failed',
            'error': errors,
            },
            safe=False)
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def delete_hall(request):
    Hall.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('hall'))



def housekeeping_hallView(request):
    id = request.GET.get('id') or None
    if request.user.is_authenticated:
        return render(request,'hotelManagement/housekeepingHall.html',{
            'form': HousekeepingForHallForm(),
            'id':id,
            'employees':Employee.objects.all(),
            'halls':Hall.objects.all(),
            'housekeeping_statuses':HousekeepingStatus.objects.all(),
        })

    return HttpResponseRedirect(reverse('login'))

def get_housekeeping_hall(request):
    if (request.GET.get('pk')):
        housekeeping = HousekeepingForHall.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(housekeeping.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = HousekeepingForHall.objects.all()

    #if user want specific housekeeping
    if request.GET.get('filter') == 'True':
        if request.GET.get('assigned_to'):
            user_query = request.GET.get('assigned_to')
            if user_query[-1] == ',':
                user_query = user_query[:-1]
            list = set(user_query.split(','))
            data = data.filter(assign_to__in = list)
        if request.GET.get('hall_number'):
            user_query = request.GET.get('hall_number')
            if user_query[-1] == ',':
                user_query = user_query[:-1]
            list = set(user_query.split(','))
            data = data.filter(hall__in = list)
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

def add_housekeeping_hall(request):
    if request.method == 'POST':
        formset = HousekeepingForHallForm(request.POST)
        if formset.is_valid():
            formset.save()

            return JsonResponse({'Result':'Succeed',},safe=False)
                        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def update_housekeeping_hall(request):
    if request.method == 'POST':
        data = request.POST
        formset = HousekeepingForHallForm(request.POST)
        housekeeping = HousekeepingForHall.objects.get(pk = data['pk'])
        if formset.is_valid():
            housekeeping.hall = Hall.objects.get(pk = data['hall'])
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

def delete_housekeeping_hall(request):
    HousekeepingForHall.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('housekeeping_hall'))



def priceManagerView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/priceManager.html',{
        })

    return HttpResponseRedirect(reverse('login'))

def get_priceManager(request):
    if request.GET.get('pk') and request.GET.get('type'):
        price = None
        if request.GET.get('type') == 'Room_Type':
            price = Room_Type.objects.get(pk = request.GET.get('pk'))
        if request.GET.get('type') == 'Hall_Type':
            price = Hall_Type.objects.get(pk = request.GET.get('pk'))
        
        return JsonResponse(price.serializePrice(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    room = Room_Type.objects.all()
    hall = Hall_Type.objects.all()
    #if user want specific price
    if request.GET.get('contain'):
        room =  Room_Type.objects.filter(title__icontains=request.GET.get('contain')).all()
        hall = Hall_Type.objects.filter(title__icontains=request.GET.get('contain')).all()

    #get from start to end posts
    data2 = []
    index = 1
    for x in room:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    for x in hall:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    return JsonResponse({
        'total_price_Manager':room.count() + hall.count(),
        'price_Manager':[x.serializePrice() for x in data2]
        },safe=False)

def update_priceManager(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        if data['type'] == 'Hall_Type':
            prices = Hall_Type.objects.get(pk = data['pk'])
        elif data['type'] == 'Room_Type':
            prices = Room_Type.objects.get(pk = data['pk'])
 
        prices.mon = data['mon']
        prices.tue = data['tue']
        prices.wed = data['wed']
        prices.thu = data['thu']
        prices.fri = data['fri']
        prices.sat = data['sat']
        prices.sun = data['sun']
        prices.save()
        return JsonResponse({'Result':'Succeed',},safe=False)

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')



def servicesView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/services.html',{
            'form': ServiceForm(),
        })

    return HttpResponseRedirect(reverse('login'))
    
def add_services(request):
    if request.method == 'POST':
        formset = ServiceForm(request.POST, request.FILES)
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

def get_services(request):
    if (request.GET.get('pk')):
        services = Service.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(services.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = Service.objects.all()

    #if user want specific room type
    if request.GET.get('contain'):
        data =  Service.objects.filter(title__icontains=request.GET.get('contain')).all()

    #get from start to end posts
    data2 = []
    index = 1
    for x in data:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    return JsonResponse({
        'total_services':data.count(),
        'services':[x.serialize() for x in data2]
        },safe=False)

def update_services(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        formset = ServiceForm(request.POST)
        services = Service.objects.get(pk = data['pk'])
        if formset.is_valid():
            for key in data:
                if key != 'active':
                    setattr(services, key, data[key])

            if 'active' in data:
                services.active = True
            else:
                services.active = False

            services.save()
            return JsonResponse({'Result':'Succeed',},safe=False)
                        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def delete_services(request):
    Service.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('services'))



def couponView(request):
    if request.user.is_authenticated:
        return render(request,'hotelManagement/coupon.html',{
            'form': CouponForm(),
            'customers': Employee.objects.all(),
            'room_types': Room_Type.objects.all(),
            'hall_types': Hall_Type.objects.all(),
        })

    return HttpResponseRedirect(reverse('login'))
    
def add_coupon(request):
    if request.method == 'POST':
        formset = CouponForm(request.POST, request.FILES)
        if formset.is_valid():
            if datetime.strptime(request.POST['start_datetime'], '%Y-%m-%dT%H:%M') >= datetime.strptime(request.POST['end_datetime'], '%Y-%m-%dT%H:%M'):
                return JsonResponse({
                    'Result':'Failed',
                    'error':'{"start_datetime": [{"message": "Start datetime must be a date before the End datetime", "code": "error"}]}'
                    },
                    safe=False)

            formset.active = "valid_only_once" in request.POST
            formset.save()
            coupon = Coupon.objects.last()
            coupon.check_availability()
            
            for x in request.POST.getlist('image'):
                coupon.image.add(Image.objects.get(pk = x))
            for x in request.POST.getlist('customer'):
                coupon.customer.add(Employee.objects.get(pk = x))
            for x in request.POST.getlist('room-type'):
                coupon.room_type.add(Room_Type.objects.get(pk = x))
            for x in request.POST.getlist('hall-type'):
                coupon.hall_type.add(Hall_Type.objects.get(pk = x))
            
            return JsonResponse({
            'Result':'Succeed',
            },
            safe=False)

        
        return JsonResponse({
            'Result':'Failed',
            'error': 'formset.errors.as_json()',
            },
            safe=False)

    return HttpResponse('Make sure that you send a post request')

def get_coupon(request):
    if (request.GET.get('pk')):
        coupon = Coupon.objects.get(pk = request.GET.get('pk'))
        return JsonResponse(coupon.serialize(), safe=False)


    start = int(request.GET.get('start') or 1)
    end = int(request.GET.get('end') or start + 4)

    data = Coupon.objects.all()

    #if user want specific room type
    if request.GET.get('contain'):
        data =  Coupon.objects.filter(title__icontains=request.GET.get('contain')).all()

    #get from start to end posts
    data2 = []
    index = 1
    for x in data:
        if index >= start  and index <= end:
            data2.append(x)
        index += 1

    for x in data2:
        x.check_availability()

    return JsonResponse({
        'total_coupon':data.count(),
        'coupon':[x.serialize() for x in data2]
        },safe=False)

def update_coupon(request):
    if request.method == 'POST':
        data = request.POST
        formset = CouponForm(request.POST)
        coupon = Coupon.objects.get(pk = data['pk'])

        if formset.is_valid():
            if datetime.strptime(request.POST['start_datetime'], '%Y-%m-%dT%H:%M') >= datetime.strptime(request.POST['end_datetime'], '%Y-%m-%dT%H:%M'):
                return JsonResponse({
                    'Result':'Failed',
                    'error':'{"start_datetime": [{"message": "Start datetime must be a date before the End datetime", "code": "error"}]}'
                    },
                    safe=False)
                
            for key in data:
                if key  != 'valid_only_once' and key != 'image' and key != 'active' and key != 'description' and key != 'customer' and key != 'room_type' and key != 'hall_type':
                    setattr(coupon, key, data[key])

            if 'valid_only_once' in data:
                coupon.valid_only_once = True
            else:
                coupon.valid_only_once = False

            coupon.description = data['description']

            coupon.image.clear()
            for x in data.getlist('image'):
                coupon.image.add(Image.objects.get(pk = x))
            
            coupon.customer.clear()
            for x in data.getlist('customer'):
                coupon.customer.add(Employee.objects.get(pk = x))

            coupon.room_type.clear()
            for x in data.getlist('room-type'):
                coupon.room_type.add(Room_Type.objects.get(pk = x))

            coupon.hall_type.clear()
            for x in data.getlist('hall-type'):
                coupon.hall_type.add(Hall_Type.objects.get(pk = x))

            coupon.check_availability()
            coupon.save()
            return JsonResponse({'Result':'Succeed',},safe=False)


        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def delete_coupon(request):
    Coupon.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('coupon'))

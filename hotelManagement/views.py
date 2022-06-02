from django.shortcuts import render, reverse
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from .models import *

# Create your views here.

def indexView(request):
    return render(request,'hotelManagement/index.html')

def room_typeView(request):
    return render(request,'hotelManagement/roomType.html',{
        'form': Room_TypeForm(),
    })

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
        data =  Room_Type.objects.filter(Title__icontains=request.GET.get('contain')).all()

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
    return render(request,'hotelManagement/floor.html',{
        'form': FloorForm(),
    })

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
    return render(request,'hotelManagement/amenity.html',{
        'form': AmenityForm(),
    })

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

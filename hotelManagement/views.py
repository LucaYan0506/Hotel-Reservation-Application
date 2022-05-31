from math import floor
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
        formset = Room_TypeForm(request.POST)
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

def get_root_type(request):
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

def update_root_type(request):
    if request.method == 'POST':
        data = request.POST
        room_type = Room_Type.objects.get(pk = data['pk'])
        formset = Room_TypeForm(request.POST)
        if formset.is_valid():
            for key in data:
                setattr(room_type, key, data[key])
            room_type.save()
            return JsonResponse({'Result':'Succeed',},safe=False)
                        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)
        
    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')


def delete_root_type(request):
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
            formset.save()
            return JsonResponse({
            'Result':'Succeed',
            },
            safe=False)

        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors['Number'],
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
        formset = Room_TypeForm(request.POST)
        floor = Floor.objects.get(pk = data['pk'])
        if formset.is_valid():
            for key in data:
                setattr(floor, key, data[key])
            floor.Active = "Active" in data
            floor.save()

            return JsonResponse({'Result':'Succeed',},safe=False)
                        
        return JsonResponse({
            'Result':'Failed',
            'error': formset.errors.as_json(),
            },
            safe=False)
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that you sent a POST request')

def delete_floor(request):
    Floor.objects.get(pk = request.GET.get('pk')).delete()

    return HttpResponseRedirect(reverse('floor'))

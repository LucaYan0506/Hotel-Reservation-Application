from django.shortcuts import render, reverse
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from .models import *
# Create your views here.

def indexView(request):
    return render(request,'hotelManagement/index.html')

def room_typeView(request):
    return render(request,'hotelManagement/roomType.html',{
        'form': Room_TypeForm(),
        'roomType': Room_Type.objects.all()
    })

def add_room_type(request):
    if request.method == 'POST':
        formset = Room_TypeForm(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('room_types'))

        return JsonResponse({
            'Result':'Failed'},
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
        for key in data:
            setattr(room_type, key, data[key])
        room_type.save()

        return HttpResponseRedirect(reverse('room_types'))
        

    return HttpResponse('You are in the wrong place, this an api only for POST request, make sure that the is a POST request')

def delete_root_type(request):
    Room_Type.objects.get(pk = request.GET.get('pk')).delete()
    
    return HttpResponseRedirect(reverse('room_types'))


       
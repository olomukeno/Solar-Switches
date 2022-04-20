import time

from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from datetime import datetime, timedelta, date
from rest_framework import serializers


def home(request):
    # print(Switches.objects.get(id=1))
    # print(Switches.objects.get(id=2))
    x = list(Switches.objects.filter(state='start').values('id', 'state', 'time_to_end', 'name')) + list(
        Switches.objects.filter(state='pause').values('id', 'state', 'pause_time', 'name'))
    context = sorted(x, key=lambda z: z['id'])

    # print(context[0]['id'])
    # print(context)
    # print(request.POST)
    if request.method == "POST":
        if request.POST.get('start'):
            obj = Switches.objects.get(id=int(request.POST.get('start')))

            if obj.pause_time is not None:
                para = str(obj.pause_time).split(':')
                obj.time_to_end = datetime.now() + timedelta(hours=int(para[0]), minutes=int(para[1]),
                                                             seconds=int(para[2][:2]))
            # else:
            #     hours = int(request.POST.get('hours'))
            #     mins = int(request.POST.get('mins'))
            # print(datetime.datetime.now().strftime("%H:%M:%S"))
            # date_later = datetime.now() + timedelta(hours=hours, minutes=mins)
            # print(datetime.combine(date.min, date_later) - datetime.combine(date.min, date_now.time()))
            obj.pause_time = None
            obj.state = 'start'
            # obj.name = request.POST.get('name')
            # obj.ttl = f"{request.POST.get('hours')}:{request.POST.get('mins')}:00"
            obj.save()
            # x = Logs.objects.create(log_date=date.today(), log=f'Station {obj.id} opened for {obj.name}')
            # x.save()
            # return redirect('main-home')

            # toggle switch on
        elif request.POST.get('pause'):
            obj = Switches.objects.get(id=int(request.POST.get('pause')))
            if obj.time_to_end is not None:
                obj.pause_time = obj.time_to_end - datetime.now()
                para = str(obj.pause_time).split(':')
                x = Logs.objects.create(log=f"Station {obj.id} paused with {para[0]} hour(s), {para[1]} minutes and "
                                            f"{para[2][2]} seconds left")
                x.save()
            obj.state = 'pause'
            obj.time_to_end = None
            # print(obj.pause_time)
            obj.save()
            # x = Logs.objects.create(log_date=date.today(), log=f'Station {obj.id} paused for {obj.name}')
            # x.save()
            # return redirect('main-home')

            # toggle switch off
        elif request.POST.get('reset'):
            obj = Switches.objects.get(id=int(request.POST.get('reset')))
            x = Logs.objects.create(log=f'Station {obj.id} reset for {obj.name}')
            x.save()
            obj.state = 'reset'
            obj.pause_time = None
            obj.time_to_end = None
            obj.name = None
            obj.ttl = None
            obj.save()
            # return redirect('main-home')

            # toggle switch off

        elif request.POST.get('save'):
            # print(request.POST)
            obj = Switches.objects.get(id=int(request.POST.get('save')))
            if obj.pause_time is not None:
                p = Saves.objects.create(name=obj.name, time_left=obj.pause_time, station_no=obj.id)
                p.save()
            else:
                pause_time = obj.time_to_end - datetime.now()
                p = Saves.objects.create(name=obj.name, time_left=pause_time, station_no=obj.id)
                p.save()
            x = Logs.objects.create(log=f'Instance of Station {obj.id} saved for {obj.name}')
            x.save()
            time.sleep(1)
            obj.state = 'reset'
            obj.pause_time = None
            obj.time_to_end = None
            obj.name = None
            obj.ttl = None
            obj.save()
            # messages.success(request, 'Data has been saved')

            # return redirect('main-home')

    # print(context)
    return render(request, 'switches/home.html', {'items': context})


def save(request):
    context = list(Saves.objects.values('id', 'name', 'time_left', 'station_no'))

    if request.method == 'POST':
        if request.POST.get('load'):
            save_form = Saves.objects.get(id=int(request.POST.get('value')))
            obj = Switches.objects.get(id=save_form.station_no)
            # print(obj.state)
            if obj.state == 'reset':
                para = str(save_form.time_left).split(':')
                date_later = datetime.now() + timedelta(hours=int(para[0]), minutes=int(para[1]),
                                                        seconds=int(para[2][:2]))
                obj.time_to_end = date_later
                obj.state = 'start'
                obj.name = save_form.name
                obj.ttl = save_form.time_left
                obj.save()
                time.sleep(1)
                x = Logs.objects.create(log=f'Saved Station {obj.id} loaded for {obj.name}')
                x.save()
                save_form.delete()

                messages.success(request, 'Saved data loaded!')
            else:
                messages.warning(request, f'Station {save_form.station_no} is in use!')
            return redirect('main-save')

        elif request.POST.get('delete'):
            save_form = Saves.objects.get(id=int(request.POST.get('value')))
            x = Logs.objects.create(log=f'Instance of Station {save_form.station_no} deleted for {save_form.name}')
            x.save()
            save_form.delete()
            messages.info(request, 'Saved data deleted')
            return redirect('main-save')

    return render(request, 'switches/save.html', {'items': context})


# def logs(request):
#     global log_time
#
#     def test(val):
#         change = []
#         context_1 = Switches.objects.filter(state='start').values('time_to_end', 'ttl')
#         data = Switches.objects.filter(state='start').values('id')
#         context_2 = Switches.objects.filter(state='pause').values('pause_time', 'ttl')
#         # print(context_1)
#         for obj in context_1:
#             print(obj['time_to_end'])
#             change = [int(val.split(':')[0]), int(val.split(':')[1]), int(val.split(':')[2])]
#             x = str(obj['time_to_end'] - datetime.now())
#             y = str(timedelta(hours=int(obj['ttl'].split(':')[0]) - int(x.split(':')[0]),
#                               minutes=int(obj['ttl'].split(':')[1]) - int(x.split(':')[1]),
#                               seconds=int(obj['ttl'].split(':')[2][:2]) - int(x.split(':')[2][:2])))
#             change[0] += int(y.split(':')[0])
#             change[1] += int(y.split(':')[1])
#             change[2] += int(y.split(':')[2])
#
#         for obj in context_2:
#             change = [int(val.split(':')[0]), int(val.split(':')[1]), int(val.split(':')[2])]
#             # x = str(datetime.strptime(obj['pause_time'], '%H:%M:%S') - datetime.now())
#             y = str(timedelta(hours=int(obj['ttl'].split(':')[0]) - int(obj['pause_time'].split(':')[0]),
#                               minutes=int(obj['ttl'].split(':')[1]) - int(obj['pause_time'].split(':')[1]),
#                               seconds=int(obj['ttl'].split(':')[2][:2]) - int(obj['pause_time'].split(':')[2][:2])))
#             change[0] += int(y.split(':')[0])
#             change[1] += int(y.split(':')[1])
#             change[2] += int(y.split(':')[2])
#             # print(change)
#
#         return change
#
#     try:
#         value = Time.objects.get(login_date=date.today())
#         context = test(value.total_time)
#         log_time = f'{context[0]}:{context[1]}:{context[2]}'
#         value.total_time = log_time
#         value.save()
#     except Time.DoesNotExist:
#         value = Time.objects.create(login_date=date.today())
#         context = test('00:00:00')
#         log_time = f'{context[0]}:{context[1]}:{context[2]}'
#         value.total_time = log_time
#         value.save()
#     # value = Time.objects.get_or_create(login_date=date.today())
#     # value.
#
#     # context = list(Logs.objects.values('log', 'log_date'))
#
#     return render(request, 'switches/logs.html', {'items': log_time})


def start(request):
    context = list(Switches.objects.filter(state='reset').values('id'))
    names = list(Saves.objects.values('name')) + list(Switches.objects.filter(state='start').values('name')) + list(
        Switches.objects.filter(state='pause').values('name'))
    names = [x['name'] for x in names]

    if request.method == "POST":
        if request.POST.get('start'):
            obj = Switches.objects.get(id=int(request.POST.get('station_no')))

            x = Logs.objects.create(
                log=f"Station {request.POST.get('station_no')} started for {request.POST.get('name')} for "
                    f"{request.POST.get('hours')} hour(s) {request.POST.get('mins')} minutes")
            x.save()

            hours = int(request.POST.get('hours'))
            mins = int(request.POST.get('mins'))
            date_later = datetime.now() + timedelta(hours=hours, minutes=mins)

            obj.time_to_end = date_later
            obj.state = 'start'
            obj.name = request.POST.get('name')
            obj.ttl = f"{request.POST.get('hours')}:{request.POST.get('mins')}:00.0"
            obj.save()
            messages.info(request, f'Station {request.POST.get("station_no")} has been activated')
            return redirect('main-start')
        # print(context)

    return render(request, 'switches/start.html', {'items': context, 'names': names})


def logs(request):
    context = list(Logs.objects.values('log', 'log_date'))

    return render(request, 'switches/logs.html', {'items': context})

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from collections import OrderedDict
from .models import obj, sens, values_sens, user_obj, param
from .forms import LogForm, Form, Panel
import datetime

def index(request):
    if request.user.is_authenticated:
        return redirect('lk')
    else:
        form = LogForm
        context =  {'form' : form}
        return render(request, 'grr/index.html', context)

def indexerr(request):
    if request.user.is_authenticated:
        return redirect('lk')
    else:
        form = LogForm
        context =  {'form' : form}
        return render(request, 'grr/indexerr.html', context)

def lk(request):
    us = request.user
    user_obj_list = user_obj.objects.all()
    user_obj_list = user_obj_list.filter(userfk = us)
    obj_list = obj.objects.none()
    for val in user_obj_list:
        list = obj.objects.all()
        list = list.filter(name = val.objfk.name)
        obj_list = obj_list.union(list)
    sens_list = sens.objects.none()
    for val in obj_list:
        list = sens.objects.all()
        list = list.filter(objfk = val)
        sens_list = sens_list.union(list)
    tp = []
    for senss in sens_list:
        ch = False
        for i in tp:
            if i == senss.type:
                ch = True
        if ch != True: tp.append(senss.type)
    form = Form()
    context =  {'obj_list' : obj_list, 'sens_list' : sens_list, 'form' : form, 'tp' : tp, 'us' : us}
    return render(request, 'grr/lk.html', context)

def lkkk(request):
    obj_list = obj.objects.all()
    sens_list = sens.objects.all()
    values_list = values_sens.objects.all()
    tp = [sens_list[0].type]
    ln = []
    for senss in sens_list:
        ch = False
        for i in tp:
            if i == senss.type:
                ch = True
        if ch != True: tp.append(senss.type)
    form = Form()
    context =  {'obj_list' : obj_list, 'sens_list' : sens_list, 'form' : form, 'tp' : tp}
    return render(request, 'grr/lk.html', context)

def grathall(request, tp, objid):
    sensl = sens.objects.all()
    sensl = sensl.filter(objfk = objid)
    sensl = sensl.filter(type = tp)
    val = []
    for se in sensl:
        values_list = values_sens.objects.all()
        val.append(values_list.filter(sensfk = se.id))
    values = []
    for i, vals in enumerate(val):
        valuessens = []
        valuessens.append(sensl[i])
        for v in vals:
            qwe = values_sens()
            qwe.dat = v.dat.strftime('%Y-%m-%d %H:%M:%S')
            qwe.tem = int(v.tem)
            valuessens.append(qwe)
        values.append(valuessens)
    context =  {'values' : values}
    return render(request, 'grr/grathall.html', context)

def timech(request, sensid):
    senstype = sens.objects.all()
    senstype = senstype.filter(id = sensid)
    senstype = senstype[0].paramfk.unit
    values_list = values_sens.objects.all()
    values_list = values_list.filter(sensfk = sensid)
    form = Form()
    context =  {'form' : form, 'sensid' : sensid, 'values_list' : values_list, 'senstype' : senstype}
    return render(request, 'grr/timech.html', context)

def grath(request, sensid):
    qwe = values_sens.objects.all()
    qwe = qwe.filter(sensfk = sensid)
    values_x = []
    values_y = []
    for qwe.test in qwe:
        values_x.append(qwe.test.dat.strftime('%Y-%m-%d %H:%M:%S'))
        values_y.append(int(qwe.test.tem))
    context =  {'values_x' : values_x, 'values_y' : values_y}
    return render(request, 'grr/googletemp.html', context)

def grathtime(request, sensid):
    time = datetime.datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
    qwe = values_sens.objects.all()
    qwe = qwe.filter(sensfk = sensid)
    values = []
    for qwe.test in qwe:
        if qwe.test.dat.date() == time:
            values = values + [(qwe.test.dat, int(qwe.test.tem))]
    context =  {'values' : values}
    return render(request, 'grr/googletemp.html', context)

@require_POST
def logg (request):
    username = request.POST['login']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('lk')
        else:
            return redirect('indexerr')
    else:
        return redirect('indexerr')

def loggout (request):
    logout(request)
    return redirect('index')

def panel(request):
    form = Panel()
    return render(request, 'grr/panel.html', {'form' : form})

@csrf_exempt
def send(request):
    mod = values_sens()
    mod.tem = float(request.POST['tem'])
    mod.dat = datetime.datetime.now()
    mod.sensfk = sens.objects.get(id=request.POST['sensfk'])
    mod.save()
    return redirect('index')

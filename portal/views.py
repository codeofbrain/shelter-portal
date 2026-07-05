from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Announcement, MaintenanceRequest, CleaningDuty, CleaningArea, CustomUser, AnnouncementComments
from .forms import MaintenanceForm, AnnouncementForm, AnnouncementCommentsForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from datetime import date
from django.http import Http404


def news(request):
    news = Announcement.objects.all().order_by('-data_posted')
    comments_form = AnnouncementCommentsForm()
    username_parts = request.user.username.split('_')
    room_number = username_parts[0] if len(username_parts) > 1 else '_'
    user_name = username_parts[1] if len(username_parts) > 1 else '_'
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.owner = request.user
            announcement.room_number = room_number
            announcement.save()
            return redirect('portal:news')
    else:
        form = AnnouncementForm()

    context = {'form': form, 'comments_form': comments_form, 'user_name': user_name, 'room_number': room_number,'news':news}
    return render(request,'portal/news.html',context)


def edit_new(request,new_id):
    new = Announcement.objects.get(id=new_id)

    if request.method != 'POST':
        form_edit_new = AnnouncementForm(instance=new)
    else:
        form_edit_new = AnnouncementForm(instance=new,data=request.POST)
        if form_edit_new.is_valid():
            form_edit_new.save()
            return redirect('portal:news')
    context = {'new':new,'form_edit_new':form_edit_new}
    return render(request,'portal/edit_new.html',context)


def comments(request,pk):
    anzeige = Announcement.objects.get(id=pk)
    if request.method != 'POST':
        form = AnnouncementCommentsForm()
    else:
        form = AnnouncementCommentsForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.announcement = anzeige
            new_comment.owner = request.user
            new_comment.save()
            return redirect('portal:news')
    context = {'anzeige':anzeige,'form':form}
    return redirect('portal:news')



def index(request):
    return render(request,'portal/index.html')



@login_required()
def main(request):
    user = request.user
    if user.master:
        return redirect('portal:main_for_masters')
    return render(request,'portal/main.html')



def about(request):
    return render(request,'portal/about.html')


def volunteer(request):
    return render(request,'portal/volunteer.html')


def utility(request):
    return render(request,'portal/utility.html')


@user_passes_test(lambda u: u.is_authenticated and u.bewohner)
def maintenance(request):
    username_parts = request.user.username.split('_')
    room_number = username_parts[0] if len(username_parts) > 1 else '_'
    user_name = username_parts[1] if len(username_parts) > 1 else '_'
    user_requests = MaintenanceRequest.objects.filter(user_name=request.user,status__in=['new','in_progress']).order_by('date_added')
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            repair_request = form.save(commit=False)
            repair_request.user_name = request.user
            repair_request.room_number = room_number
            repair_request.save()
            messages.success(request, 'Ihre Anfrage wurde erfolgreich übermittelt')
            return redirect('portal:maintenance')

    else:
        form = MaintenanceForm(initial={'room_number': room_number, 'user_name': user_name})

    context = {'form':form,'user_name':user_name,'room_number':room_number,'user_requests':user_requests}
    return render(request,'portal/maintenance.html',context)



def putzplan(request):
    areas = CleaningArea.objects.all()
    weeks = CleaningDuty.objects.values('date_start','date_end').distinct().order_by('date_start')
    username_parts = request.user.username.split('_')
    room_number = username_parts[0] if len(username_parts) > 1 else '_'
    matrix = []
    for area in areas:
        area_dutes = {}
        duties = CleaningDuty.objects.filter(area=area)
        for duty in duties:
            area_dutes[duty.date_start] = duty
        matrix.append({'area' : area, 'duties_by_week' : area_dutes})
    context = {'weeks': weeks , 'matrix':matrix, 'current_day': date.today(),'room_number':room_number}
    return render(request,'portal/putzplan.html',context)



@login_required()
def change_duty_status(request,pk):
    if not request.user.is_staff:
        return redirect('portal:putzplan')
    duty = get_object_or_404(CleaningDuty,id=pk)

    if duty.status == 'waiting' or not duty.status:
        duty.status = 'done'
    elif duty.status == 'done':
        duty.status = 'failed'
    else:
        duty.status = 'waiting'
    duty.save()
    return redirect('portal:putzplan')



@user_passes_test(lambda u: u.is_authenticated and u.master)
def master_list(request):
    active_requests = MaintenanceRequest.objects.filter(status='new').order_by('user_name')
    context = {'active_requests':active_requests}
    return render(request,'portal/master_list.html', context)


@user_passes_test(lambda u: u.is_authenticated and u.master)
def task_in_progress(request):
    active_requests = MaintenanceRequest.objects.filter(status='in_progress').order_by('user_name')
    context = {'active_requests':active_requests}
    return render(request,'portal/task_in_progress.html', context)


@user_passes_test(lambda u: u.is_authenticated and u.master)
def master_list_arhiv(request):
    active_requests = MaintenanceRequest.objects.filter(status='done').order_by('user_name')
    context = {'active_requests':active_requests}
    return render(request,'portal/master_list_arhiv.html', context)



def complete_request(request,pk):
   claim = MaintenanceRequest.objects.get(id=pk)
   claim.status = 'done'
   claim.save()
   return redirect('portal:master_list_arhiv')


def in_progress(request,pk):
   claim = MaintenanceRequest.objects.get(id=pk)
   claim.status = 'in_progress'
   claim.save()
   return redirect('portal:task_in_progress')


def canceled_tasks(request):
    canceled_tasks = MaintenanceRequest.objects.filter(status='none').order_by('user_name')
    context = {'canceled_tasks': canceled_tasks}
    return render(request, 'portal/canceled_tasks.html', context)


def task_cancel(request,pk):
    claim = MaintenanceRequest.objects.get(id=pk)
    claim.status = 'none'
    claim.save()
    messages.warning(request,'Ваша заявка успешно отменена')
    return redirect('portal:maintenance')


@user_passes_test(lambda u: u.is_authenticated and u.master)
def main_for_masters(request):
    return render(request,'portal/main_for_masters.html')





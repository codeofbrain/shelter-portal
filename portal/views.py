from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Announcement, MaintenanceRequest, CleaningDuty, CleaningArea, CustomUser, AnnouncementComments
from .forms import MaintenanceForm, AnnouncementForm, AnnouncementCommentsForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from datetime import date
from django.http import Http404
from django.views.decorators.http import require_POST
from django.urls import reverse
from accounts.templatetags.decorators import user_required
from django.utils import timezone
from django.utils.dateparse import parse_datetime

@login_required()
@user_required('bewohner')
def news(request):
    news = Announcement.objects.all().order_by('-data_posted')
    comments_form = AnnouncementCommentsForm()
    username_parts = request.user.username.split('_')
    room_number = username_parts[0] if len(username_parts) > 1 else '_'
    user_name = username_parts[1] if len(username_parts) > 1 else '_'
    request.user.last_news_visit = timezone.now()
    request.user.save(update_fields=['last_news_visit'])
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
    form_edit_com = None
    edit_com_id = request.GET.get('edit_com_id')

    if edit_com_id:
        comment_to_edit = AnnouncementComments.objects.filter(id=edit_com_id).first()
        form_edit_com = AnnouncementCommentsForm(instance=comment_to_edit)
    context = {'form': form, 'comments_form': comments_form, 'user_name': user_name, 'room_number': room_number,'news':news, 'form_edit_com': form_edit_com, 'edit_com_id': edit_com_id}
    return render(request,'portal/news.html',context)


def edit_new(request,new_id):
    new = get_object_or_404(Announcement, id=new_id)

    if request.method == 'POST':
        form_edit_new = AnnouncementForm(data=request.POST, instance=new)
        if form_edit_new.is_valid():
            form_edit_new.save()
            return redirect('portal:news')
    else:
        form_edit_new = AnnouncementForm(instance=new)
    context = {'new':new,'form_edit_new':form_edit_new}
    return render(request,'portal/edit_new.html',context)


@require_POST
def delete_new(request, new_id):
    new = get_object_or_404(Announcement, id=new_id)
    new.delete()
    return redirect('portal:news')


@require_POST
def comments(request,pk):
    anzeige = get_object_or_404(Announcement, id=pk)
    form = AnnouncementCommentsForm(data=request.POST)

    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.announcement = anzeige
        new_comment.owner = request.user
        new_comment.save()

    return redirect('portal:news')

@require_POST
def edit_comment(request, com_id):
    comment = get_object_or_404(AnnouncementComments, id=com_id)
    form_edit_com = AnnouncementCommentsForm(instance=comment, data=request.POST)
    if form_edit_com.is_valid():
        form_edit_com.save()
    return redirect(f"{reverse('portal:news')}?open_news_id={comment.announcement.id}#comment-{comment.id}")

@require_POST
def delete_comment(request, com_id):
    comment = get_object_or_404(AnnouncementComments, id=com_id)
    new_id = comment.announcement.id
    comment.delete()
    return redirect(f'/news/?open_news_id={new_id}')


def index(request):
    return render(request,'portal/index.html')



@login_required()

def main(request):

    last_visit = request.user.last_news_visit

    if last_visit:
        new_news_count = Announcement.objects.filter(data_posted__gt=last_visit).count()
    else:
        new_news_count = Announcement.objects.count()

    user = request.user
    if user.leiterin:
        if not request.GET.get('bypass'):
            return redirect('portal:main_for_staff')
    elif user.master or user.is_superuser:
        print(f'{user.username} | master = {user.master} | leiterin = {user.leiterin} | bewohner = {user.bewohner}')
        return redirect('portal:main_for_masters')
    context = {'new_news_count': new_news_count}
    return render(request,'portal/main.html',context)




def about(request):
    return render(request,'portal/about.html')

@login_required()
@user_required('bewohner')
def volunteer(request):
    return render(request,'portal/volunteer.html')

@login_required()
@user_required('bewohner')
def utility(request):
    return render(request,'portal/utility.html')


@login_required()
@user_required('bewohner')
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
            messages.success(request, 'Ihre Anfrage wurde erfolgreich übermittelt.<br>Ваш запит успішно надіслано')
            return redirect('portal:maintenance')

    else:
        form = MaintenanceForm(initial={'room_number': room_number, 'user_name': user_name})

    context = {'form':form,'user_name':user_name,'room_number':room_number,'user_requests':user_requests}
    return render(request,'portal/maintenance.html',context)


@login_required()
@user_required('bewohner')
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



@login_required()
@user_required('master')
def master_list(request):
    active_requests = MaintenanceRequest.objects.filter(status='new').order_by('user_name')
    context = {'active_requests':active_requests}
    request.user.last_new_aufgaben_list_visit = timezone.now()
    request.user.save(update_fields=['last_new_aufgaben_list_visit'])
    return render(request,'portal/master_list.html', context)


@login_required()
@user_required('master')
def task_in_progress(request):
    active_requests = MaintenanceRequest.objects.filter(status='in_progress').order_by('user_name')
    context = {'active_requests':active_requests}
    return render(request,'portal/task_in_progress.html', context)


@login_required()
@user_required('master')
def master_list_arhiv(request):
    active_requests = MaintenanceRequest.objects.filter(status='done').order_by('user_name')
    context = {'active_requests':active_requests}
    return render(request,'portal/master_list_arhiv.html', context)


@login_required()
@require_POST
def complete_request(request,pk):
   claim = get_object_or_404(MaintenanceRequest, id=pk)
   claim.status = 'done'
   claim.save()
   return redirect('portal:master_list_arhiv')


@login_required()
@require_POST
def in_progress(request,pk):
   claim = get_object_or_404(MaintenanceRequest, id=pk)
   claim.status = 'in_progress'
   claim.save()
   return redirect('portal:task_in_progress')


@login_required()
@user_required('master')
def canceled_tasks(request):
    canceled_tasks = MaintenanceRequest.objects.filter(status='none').order_by('user_name')
    context = {'canceled_tasks': canceled_tasks}
    return render(request, 'portal/canceled_tasks.html', context)

@login_required()
@user_required('bewohner')
def task_cancel(request,pk):
    claim = get_object_or_404(MaintenanceRequest, id=pk)
    claim.status = 'none'
    claim.save()
    messages.warning(request,'Ihre Anfrage wurde erfolgreich storniert.<br>Ваш запит успішно скасовано.')
    return redirect('portal:maintenance')


@login_required()
@user_required('master')
def main_for_masters(request):
    last_visit = request.user.last_new_aufgaben_list_visit

    if last_visit:
        new_aufgaben_count = MaintenanceRequest.objects.filter(staus='new',date_added__gt=last_visit).count()
    else:
        new_aufgaben_count = MaintenanceRequest.objects.filter(status='new').count()
    context = {'new_aufgaben_count': new_aufgaben_count}
    return render(request,'portal/main_for_masters.html',context)


@login_required()
@user_required('bewohner')
def rules(request):
    return render(request,'portal/rules.html')

@login_required()
@user_required('leiterin')
def main_for_staff(request):
    return render(request,'portal/main_for_staff.html')


@login_required()
@user_required('bewohner')
def diakonie(request):
    return render(request,'portal/diakonie.html')
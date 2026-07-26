from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from .forms import HotelRegisterForm
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib import messages


def register(request):
    if request.method != 'POST':
        form = HotelRegisterForm()
    else:
        form = HotelRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, 'Melden Sie sich bitte beim Administrator. / Будь ласка, зверніться до адміністратора.')
            return redirect('portal:index')

    context = {'form':form}
    return render(request,'accounts/register.html',context)

@user_passes_test(lambda u: u.is_authenticated and u.is_superuser)
def user_confirm(request,user_id):
    User = get_user_model()
    guest = get_object_or_404(User,id=user_id)
    guest.is_active = True
    guest.save()

    return redirect('accounts:confirmed_users')

@user_passes_test(lambda u: u.is_authenticated and u.is_superuser)
def new_register_view(request):
    User = get_user_model()
    inactive_users = User.objects.filter(is_active=False)
    context = {'inactive_users': inactive_users}
    return render(request,'accounts/new_user.html',context)

@user_passes_test(lambda u: u.is_authenticated and u.is_superuser)
def confirmed_users(request):
    User = get_user_model()
    active_users = User.objects.filter(is_active=True)
    context = {'active_users': active_users}
    return render(request,'accounts/confirmed_users.html',context)
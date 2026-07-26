from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django import forms
User = get_user_model()

class HotelLoginForm(AuthenticationForm):
    field_order = ['room_number','username','password']
    room_number = forms.CharField(
        label='Room number',
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Room number'})
        )

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Username'})
        self.fields['password'].widget.attrs.update({'class':'form-control','placeholder':'Password'})
        fields = list(self.fields.keys())
        fields.insert(0,fields.pop(fields.index(('room_number'))))
        self.fields = {key : self.fields[key] for key in fields}

    def clean(self):
        room_number = self.cleaned_data.get('room_number','').strip()
        user_name = self.cleaned_data.get('username','').strip()
        print('test')
        print(room_number)
        print(user_name)
        if room_number and user_name:
            self.cleaned_data['username'] = f'{room_number}_{user_name}'
        else:
            self.cleaned_data['username'] = user_name
        print(f'{room_number}_{user_name}')
        return super().clean()


class HotelRegisterForm(UserCreationForm):
    field_order = ['room_number','username','password','password']
    room_number = forms.CharField(
        label='Room number',
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Room number'})
        )

    class Meta(UserCreationForm.Meta):
        User = get_user_model()
        model = User
        fields = UserCreationForm.Meta.fields

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Username'})
        self.fields['username'].help_text=False
        fields = list(self.fields.keys())
        fields.insert(0,fields.pop(fields.index(('room_number'))))
        self.fields = {key : self.fields[key] for key in fields}

    def clean(self):
        cleaned_data = super().clean()
        room_number = cleaned_data.get('room_number','').strip()
        user_name = self.cleaned_data.get('username','').strip()

        if room_number and user_name:
            full_username = f'{room_number}_{user_name}'
            if User.objects.filter(username=full_username).exists:
                raise forms.ValidationError('Ein benutzer mit dieser Zimmernummer und diesem Namen existiert bereits')
        return cleaned_data

    def save(self,commit=True):
        user = super().save(commit=False)
        room_number = self.cleaned_data.get('room_number','').strip()
        username = self.cleaned_data.get('username','').strip()
        user.is_active = False

        if room_number and username:
            user.username = f'{room_number}_{username}'
        else:
            user.username = username

        if commit:
            user.save()
        return user
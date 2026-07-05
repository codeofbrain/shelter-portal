
from django import forms
from .models import MaintenanceRequest, Announcement, AnnouncementComments

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['description']


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['content']

class AnnouncementCommentsForm(forms.ModelForm):
    class Meta:
        model = AnnouncementComments
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'rows': 2,
                'placeholder':'Ihr Kommentar...'
            })
        }
        labels = {
            'comment': '',
        }
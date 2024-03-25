from django import forms
from django.utils.translation import gettext as _
from entries.models import Entry
from projects.models import Project


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ['description', 'project',
                  'start_time', 'start_date',
                  'finish_time', 'finish_date']

    def __init__(self, user, project=None, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(owner=user)
        if project:
            self.fields['project'].initial = project

    def clean(self):
        cleaned_data = super(EntryForm, self).clean()
        finish_date = cleaned_data.get('finish_date')
        start_date = cleaned_data.get('start_date')
        if finish_date < start_date:
            self.add_error('finish_date', _('Finish date should be after start date or same day'))
        finish_time = cleaned_data.get('finish_time')
        start_time = cleaned_data.get('start_time')
        if finish_time < start_time:
            self.add_error('finish_time', _('Finish time should be after start time'))



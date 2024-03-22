from django import forms

from entries.models import Entry
from projects.models import Project


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ['description', 'project',
                  'start_time', 'start_date',
                  'finish_time', 'finish_date']

    def __init__(self, user, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(owner=user)

from django import forms

from projects.models import Project
from customers.models import Customer

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'customer', 'is_billable', 'weekly_goal']

    def __init__(self, user, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(owner=user)
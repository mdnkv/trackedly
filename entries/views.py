from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import request

from djqscsv import render_to_csv_response

from entries.models import Entry
from entries.forms import EntryForm
from projects.models import Project


class EntryCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = EntryForm
    template_name = 'entries/views/entry_create_view.html'
    success_url = reverse_lazy('entries:entries_list_view')

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.owner = self.request.user
        entry.save()
        message = _('Entry was created successfully!')
        messages.success(self.request, message)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EntryCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.GET.get('project_id', None):
            project_id = self.request.GET.get('project_id')
            project = Project.objects.filter(pk=project_id, owner=self.request.user).first()
            if project:
                kwargs['project'] = project
        return kwargs


class EntryUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = EntryForm
    template_name = 'entries/views/entry_update_view.html'
    success_url = reverse_lazy('entries:entries_list_view')
    context_object_name = 'entry'

    def form_valid(self, form):
        message = _('Entry was updated successfully!')
        messages.success(self.request, message)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EntryUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Entry.objects.filter(owner=self.request.user)


class EntryDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'entries/views/entry_delete_view.html'
    success_url = reverse_lazy('entries:entries_list_view')
    context_object_name = 'entry'

    def get_queryset(self):
        return Entry.objects.filter(owner=self.request.user)


class EntriesListView(LoginRequiredMixin, generic.ListView):
    template_name = 'entries/views/entries_list_view.html'
    context_object_name = 'entries'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(EntriesListView, self).get_context_data(**kwargs)
        project_id = self.request.GET.get('project_id', None)
        if project_id:
            project = Project.objects.filter(pk=project_id, owner=self.request.user).first()
            if project:
                context['selected_project'] = project
        return context

    def get_queryset(self):
        project_id = self.request.GET.get('project_id', None)
        if project_id:
            project = Project.objects.filter(pk=project_id, owner=self.request.user).first()
            if project:
                return Entry.objects.filter(project=project)
        return Entry.objects.filter(owner=self.request.user)


class EntryDetailView(LoginRequiredMixin, generic.DetailView):

    template_name = 'entries/views/entry_detail_view.html'
    context_object_name = 'entry'

    def get_queryset(self):
        return Entry.objects.filter(owner=self.request.user)

@login_required()
def entries_to_csv_view(request):
    entries = Entry.objects.filter(owner=request.user)
    return render_to_csv_response(entries)

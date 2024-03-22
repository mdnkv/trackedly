from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from entries.models import Entry
from entries.forms import EntryForm
from projects.models import Project


class EntryCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = EntryForm
    template_name = 'entries/entry_create_view.html'
    success_url = reverse_lazy('entries:entries_list_view')

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.owner = self.request.user
        entry.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EntryCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EntryUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = EntryForm
    template_name = 'entries/entry_update_view.html'
    success_url = reverse_lazy('entries:entries_list_view')
    context_object_name = 'entry'

    def get_form_kwargs(self):
        kwargs = super(EntryUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Entry.objects.filter(owner=self.request.user)


class EntryDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'entries/entry_delete_view.html'
    success_url = reverse_lazy('entries:entries_list_view')
    context_object_name = 'entry'

    def get_queryset(self):
        return Entry.objects.filter(owner=self.request.user)


class EntriesListView(LoginRequiredMixin, generic.ListView):
    template_name = 'entries/entries_list_view.html'
    context_object_name = 'entries'

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

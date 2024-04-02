from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import request

from projects.models import Project
from projects.forms import ProjectForm
from customers.models import Customer

from djqscsv import render_to_csv_response


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'projects/views/project_create_view.html'
    success_url = reverse_lazy('projects:projects_list_view')
    form_class = ProjectForm

    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()
        message = _('Project was created successfully!')
        messages.success(self.request, message)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'projects/views/project_update_view.html'
    success_url = reverse_lazy('projects:projects_list_view')
    form_class = ProjectForm
    context_object_name = 'project'

    def get_form_kwargs(self):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self,form):
        message = _('Project was updated successfully!')
        messages.success(self.request, message)
        return super().form_valid(form)

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    success_url = reverse_lazy('projects:projects_list_view')
    context_object_name = 'project'
    template_name = 'projects/views/project_delete_view.html'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class ProjectsListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'projects'
    template_name = 'projects/views/projects_list_view.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(ProjectsListView, self).get_context_data(**kwargs)
        customer_id = self.request.GET.get('customer_id', None)
        if customer_id:
            customer = Customer.objects.filter(pk=customer_id, owner=self.request.user).first()
            if customer:
                context['selected_customer'] = customer
        return context

    def get_queryset(self):
        # If project by customer are selected
        customer_id = self.request.GET.get('customer_id', None)
        if customer_id:
            # check that this customer do actually belong to the user
            customer = Customer.objects.filter(pk=customer_id, owner=self.request.user).first()
            if customer:
                return Project.objects.filter(customer=customer)
        # default queryset
        return Project.objects.filter(owner=self.request.user)


@login_required()
def projects_to_csv_view(request):
    projects = Project.objects.filter(owner=request.user)
    return render_to_csv_response(projects)

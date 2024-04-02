from django.urls import reverse_lazy

from django.views.generic import (CreateView, UpdateView, DeleteView, FormView, DetailView)
from django.contrib.auth import (get_user_model, update_session_auth_hash)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.utils.translation import gettext as _

from users.forms import (SignupForm, UserUpdateForm)

User = get_user_model()


class SignupView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('users:login_view')
    template_name = 'users/views/signup_view.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:user_detail_view')
    template_name = 'users/views/user_update_view.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        message = _('Your account data was updated successfully')
        messages.success(self.request, message)
        return super().form_valid(form)


class PasswordUpdateView(LoginRequiredMixin, FormView):
    template_name = 'users/views/password_update_view.html'
    success_url = reverse_lazy('users:user_detail_view')
    form_class = SetPasswordForm

    def get_form_kwargs(self):
        kwargs = super(PasswordUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        result = form.save()
        update_session_auth_hash(self.request, result)
        message = _('Your password was updated successfully')
        messages.success(self.request, message)
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'users/views/user_delete_view.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users:login_view')

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'users/views/user_detail_view.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

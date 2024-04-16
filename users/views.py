from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import (CreateView, UpdateView, DeleteView, FormView, DetailView, TemplateView)
from django.contrib.auth import (get_user_model, update_session_auth_hash)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.utils.translation import gettext as _

from users.forms import (SignupForm, UserUpdateForm)
from users.models import EmailConfirmation

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


def confirm_email_view(request):
    token_id = request.GET.get('token_id', None)
    if token_id is None:
        data = {'is_confirmed': False}
        return render(request, template_name='users/views/email_confirmed_view.html', context=data)
    try:
        token = EmailConfirmation.objects.get(pk=token_id)
        user = token.user
        user.is_email_confirmed = True
        user.save()
        token.delete()
        data = {'is_confirmed': True}
    except EmailConfirmation.DoesNotExist:
        data = {'is_confirmed': False}
    return render(request, template_name='users/views/email_confirmed_view.html', context=data)
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, TemplateView

from accounts.forms import RegistrationUserForm, LoginUserForm
from accounts.mixins import AccountDataMixin


@method_decorator(csrf_protect, name='dispatch')
class RegistrationUsersView(AccountDataMixin, CreateView):
    name_page = 'registration_page'
    template_name = 'account/registration.html'
    form_class = RegistrationUserForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.save()
        login(self.request, user)
        success_url = reverse('user-profile', kwargs={'slug': user.username})
        return HttpResponseRedirect(success_url)


@method_decorator(csrf_protect, name='dispatch')
class LoginUsersView(AccountDataMixin, LoginView):
    name_page = 'login_page'
    template_name = 'account/login.html'
    form_class = LoginUserForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        success_url = reverse('user-profile', kwargs={'slug': form.get_user()})
        return HttpResponseRedirect(success_url)


@method_decorator(csrf_protect, name='dispatch')
class UserForgotPasswordView(AccountDataMixin, TemplateView):
    template_name = 'account/forgot-password.html'
    name_page = 'forgot_password_page'


@csrf_protect
@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

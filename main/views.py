from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy

from django.views.generic import TemplateView,FormView,RedirectView

from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer

from braces import views as braces

from .models import User
from .forms import LoginForm, ProposalForm


##########################
#
# Auth views
#
##########################

class LoginView(FormView):
	form_class = LoginForm
	success_url = reverse_lazy('home')
	template_name = 'registration/login.html'

	def form_valid(self, form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)

		if user is not None and user.is_active:
			login(self.request, user)
			return super(LoginView, self).form_valid(form)
		else:
			return self.form_invalid(form)

class LogOutView(braces.LoginRequiredMixin,braces.MessageMixin,RedirectView):
	url = reverse_lazy('home')

	def get(self, request, *args, **kwargs):
		logout(request)
		self.messages.success("You've been logged out. Come back soon!")
		return super(LogOutView, self).get(request, *args, **kwargs)

##########################
#
# Templated views
#
##########################

class IndexView(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['form'] = ProposalForm

		return context


##########################
#
# API v1 endpoints
#
##########################

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = Group.objects.all()
	serializer_class = GroupSerializer

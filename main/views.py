from django.contrib.auth.models import Group
from django.views.generic import TemplateView

from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer

from models import User

##########################
#
# Templated views
#
##########################

class IndexView(TemplateView):
	template_name = 'index.html'


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

__author__ = 'gugs'
from django.conf.urls import url, include
from rest_framework import routers
from views import IndexView, UserViewSet, GroupViewSet, LoginView, LogOutView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	# Auth views
	url(r'^login/$', LoginView.as_view(), name='login'),
	url(r'^logout/$', LogOutView.as_view(), name='logout'),

	# Templated views
	url(r'^$', IndexView.as_view(), name='home'),

	# API/v1 views
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
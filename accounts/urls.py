from django.conf.urls import url

from .views import RegisterView, LoginProfileView, ProfileDetailView, logout_profile

app_name = 'accounts'
urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginProfileView.as_view(), name='login'),
    url(r'^logout/$', logout_profile, name='logout'),
    url(r'^(?P<username>[-\w]{5,30})$', ProfileDetailView.as_view(), name='profile'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
]

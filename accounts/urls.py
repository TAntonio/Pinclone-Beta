from django.conf.urls import url

from .views import (RegisterView, LoginProfileView, ProfileDetailView,
                    ProfileUpdateView, FollowersListView, FollowingsListView,
                    UsersListView, FollowProfileView, LogoutProfile, UnfollowProfileView)

app_name = 'accounts'
urlpatterns = [
    url(r'^$', UsersListView.as_view(), name='users'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginProfileView.as_view(), name='login'),
    url(r'^logout/$', LogoutProfile.as_view(), name='logout'),
    url(r'^(?P<username>[-\w]{2,30})/$', ProfileDetailView.as_view(), name='profile'),
    url(r'^(?P<username>[-\w]{2,30})/update/$', ProfileUpdateView.as_view(),
        name='profile_update'),
    url(r'^(?P<username>[-\w]{2,30})/followers/$', FollowersListView.as_view(),
        name='profile_followers'),
    url(r'^(?P<username>[-\w]{2,30})/followings/$', FollowingsListView.as_view(),
        name='profile_followings'),
    url(r'^(?P<username>[-\w]{2,30})/follow/$', FollowProfileView.as_view(),
        name='follow'),
    url(r'^(?P<username>[-\w]{2,30})/unfollow/$', UnfollowProfileView.as_view(),
        name='unfollow'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
]

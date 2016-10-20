from django.conf.urls import url

from .views import (RegisterView, LoginProfileView, ProfileDetailView,
                    ProfileUpdateView, logout_profile)

app_name = 'accounts'
urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginProfileView.as_view(), name='login'),
    url(r'^logout/$', logout_profile, name='logout'),
    url(r'^(?P<username>[-\w]{2,30})/$', ProfileDetailView.as_view(), name='profile'),
    url(r'^(?P<username>[-\w]{5,30})/update/$', ProfileUpdateView.as_view(),
        name='profile_update'),
    # url(r'^(?P<username>[-\w]{5,30})/followers/$', FollowersListView.as_view(),
    #     name='profile_followers'),
    # url(r'^(?P<username>[-\w]{5,30})/followings/$', FollowingsListView.as_view(),
    #     name='profile_followings'),
    # url(r'^(?P<username>[-\w]{5,30})/follow/$', FollowProfileView.as_view(),
    #     name='follow'),
    # url(r'^(?P<username>[-\w]{5,30})/unfollow/$', UnfollowProfileView.as_view(),
    #     name='unfollow'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
]

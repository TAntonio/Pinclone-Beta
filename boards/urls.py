from django.conf.urls import url

from .views import BoardsListView, BoardDetailView, BoardCreateView, BoardUpdateView, BoardDeleteView

app_name = 'board'
urlpatterns = [
    url(r'^$', BoardsListView.as_view(), name='list_of_user'),
    url(r'^create/$', BoardCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[0-9A-Za-z_\-]+)/$', BoardDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[0-9A-Za-z_\-]+)/update/$', BoardUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[0-9A-Za-z_\-]+)/delete/$', BoardDeleteView.as_view(), name='delete'),
    # url(r'^(?P<slug>[0-9A-Za-z_\-]+)/follow/$', BoardFollowView.as_view(), name='follow'),
    # url(r'^(?P<slug>[0-9A-Za-z_\-]+)/unfollow/$', BoardFollowView.as_view(), name='unfollow'),
    # url(r'^(r'^(?P<slug>[0-9A-Za-z_\-]+))/$', BoardDetailView.as_view(), name='user_list'),
]


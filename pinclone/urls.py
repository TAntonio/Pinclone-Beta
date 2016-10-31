"""pinclone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler400, handler403, handler404, handler500
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import HomepageView
from pins.views import FeedView


handler404 = 'pins.views.page_not_found'
handler500 = 'pins.views.server_error'

urlpatterns = [
    url(r'^$', HomepageView.as_view(), name='home'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^boards/', include('boards.urls')),
    url(r'^pins/', include('pins.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^feed/', FeedView.as_view(), name='feed')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


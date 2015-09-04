from django.conf.urls import include, url
from django.contrib import admin

from service.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'video.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^download/(?P<hashinfo>\w{40})/', DownloadView.as_view()),

    url(r'^retrieve/(?P<hashinfo>\w{40})/', RetrieveView.as_view()),




    url(r'^admin/', include(admin.site.urls)),
]

from django.conf.urls import include, url
from django.contrib import admin

from service.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'video.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^create/(?P<hashinfo>\w{40})/', CreateView.as_view()),
    url(r'^retrieve_all/', RetrieveAllView.as_view()),
    url(r'^retrieve/(?P<hashinfo>\w{40})/', RetrieveView.as_view()),
    url(r'^delete/(?P<hashinfo>\w{40})/', DeleteView.as_view()),

    url(r'^query/(?P<hashinfo>\w{40})/', QueryView.as_view()),






    url(r'^admin/', include(admin.site.urls)),
]

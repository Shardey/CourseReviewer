from django.conf.urls import url

from . import views

urlpatterns = [
    # /ratings/
    url(r'^$', views.index, name='index'),
    # /ratings/CS-C4000/
    url(r'^(?P<course_code>[0-9a-zA-Z\-]*)/$', views.results, name='results'),
    # Registration URLs
    url(r'^accounts/register/$', 'simplesite.views.register', name='register'),
    url(r'^accounts/register/complete/$', 'simplesite.views.registration_complete', name='registration_complete'),
]



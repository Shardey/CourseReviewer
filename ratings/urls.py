from django.conf.urls import url

from . import views

urlpatterns = [
    # /ratings/
    url(r'^$', views.index, name='index'),
    # Registration URLs
    url(r'^register/$', views.register, name='register'),
    url(r'^register/complete/$', views.registration_complete, name='registration_complete'),
    # /ratings/CS-C4000/
    # url(r'^(?P<course_code>[0-9a-zA-Z\-]*)/$', views.results, name='results'),
]



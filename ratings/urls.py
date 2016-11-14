from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # /ratings/
    url(r'^$', views.index, name='index'),
    # Auth-related URLs:
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^loggedin/$', views.loggedin, name='loggedin'),
    # Registration URLs
    url(r'^register/$', views.register, name='register'),
    url(r'^register/complete/$', views.registration_complete, name='registration_complete'),
    
    # url(r'^home/$', views.home), 
    url(r'^search/$', views.search, name='search'),
    
    # /ratings/CS-C4000/
    # url(r'^(?P<course_code>[0-9a-zA-Z\-]*)/$', views.results, name='results'),
]



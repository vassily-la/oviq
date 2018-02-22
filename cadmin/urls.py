from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'blog/login.html'}, name="login"),
    url(r'^accounts/logout/$', auth_views.logout, {'template_name': 'cadmin/logout.html'}, name="logout"),
    url(r'^post/add/$', views.post_add, name='post_add'),
    url(r'^post/update/(?P<pk>[\d]+)/', views.post_update, name='post_update'),
]

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout),
    url(r'^add_toy$', views.add_toy),
    url(r'^add_toy_process$', views.add_toy_process),
    url(r'^remove_toy_(?P<toy_id>\d+)$', views.remove_toy),
    url(r'^delete_toy_(?P<toy_id>\d+)$', views.delete_toy),
]

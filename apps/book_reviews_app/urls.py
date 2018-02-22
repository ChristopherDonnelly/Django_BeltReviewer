from django.conf.urls import url 
from . import views 
 
urlpatterns = [ 
    url(r'^$', views.index),
    url(r'^add/$', views.add),
    url(r'^add_book/$', views.add_book),
    url(r'^add_review/([0-9]{1,})/$', views.add_review),
    url(r'^users/([0-9]{1,})/$', views.users),
    url(r'^([0-9]{1,})/([0-9]{1,})/delete/$', views.delete_review),
    url(r'^([0-9]{1,})/$', views.books)
] 

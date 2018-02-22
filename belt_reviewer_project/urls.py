from django.conf.urls import url, include 
from django.contrib import admin 
 
urlpatterns = [
    url(r'^', include('apps.users_app.urls')),
    url(r'^books/', include('apps.book_reviews_app.urls')),
    url(r'^$', include('apps.book_reviews_app.urls'))
]

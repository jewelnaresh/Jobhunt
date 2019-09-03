from django.urls import path

from . import views

urlpatterns = [
    path('postjob', views.postjob, name='postjob'),
    path('update', views.scraper_view, name="scraper_view"),
    path('scraper', views.scraper, name="scraper"),
    path('', views.JobListView.as_view(), name="index"),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('api/chatbot', views.api, name='api'),
]

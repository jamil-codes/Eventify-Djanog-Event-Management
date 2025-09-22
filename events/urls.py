from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.events, name='events'),
    path('new/', views.add_event, name='add_event'),
]

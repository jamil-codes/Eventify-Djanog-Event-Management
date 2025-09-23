from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.events, name='events'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/edit', views.edit_event, name='edit_event'),
    path('new/', views.add_event, name='add_event'),
]

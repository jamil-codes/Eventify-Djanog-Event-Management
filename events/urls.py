from django.urls import path
from .views import event_views, ticket_views

app_name = 'events'
urlpatterns = [
    path('', event_views.events, name='events'),
    path('<int:pk>/', event_views.event_detail, name='event_detail'),
    path('<int:pk>/edit/', event_views.edit_event, name='edit_event'),
    path('<int:pk>/add-ticket-type/',
         ticket_views.add_ticket_type, name='add_ticket_type'),
    path('new/', event_views.add_event, name='add_event'),
]

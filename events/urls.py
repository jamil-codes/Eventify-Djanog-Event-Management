from django.urls import path
from .views import event_views, ticket_views

app_name = 'events'
urlpatterns = [
    # ----------------------  Event Views  ----------------------
    path('', event_views.events, name='events'),
    path('<int:pk>/', event_views.event_detail, name='event_detail'),
    path('<int:pk>/edit/', event_views.edit_event, name='edit_event'),
    path('new/', event_views.add_event, name='add_event'),
    path('<int:event_pk>/delete-event/',
         event_views.delete_event, name='delete_event'),

    # ----------------------  Ticket Views  ----------------------
    path('<int:event_pk>/add-ticket-type/',
         ticket_views.add_ticket_type, name='add_ticket_type'),
    path('<int:event_pk>/edit-ticket-type/<int:ticket_type_pk>/',
         ticket_views.edit_ticket_type, name='edit_ticket_type'),
    path('<int:event_pk>/delete-ticket-type/<int:ticket_type_pk>/',
         ticket_views.delete_ticket_type, name='delete_ticket_type'),
]

from django.urls import path
from .views import event_views, ticket_views

app_name = 'events'
urlpatterns = [
    # ----------------------  Event Views  ----------------------
    path('', event_views.events, name='events'),
    path('<uuid:pk>/', event_views.event_detail, name='event_detail'),
    path('<uuid:pk>/edit/', event_views.edit_event, name='edit_event'),
    path('new/', event_views.add_event, name='add_event'),
    path('<uuid:event_pk>/delete-event/',
         event_views.delete_event, name='delete_event'),

    # ----------------------  Ticket Views  ----------------------
    path('<uuid:event_pk>/add-ticket-type/',
         ticket_views.add_ticket_type, name='add_ticket_type'),
    path('<uuid:event_pk>/edit-ticket-type/<uuid:ticket_type_pk>/',
         ticket_views.edit_ticket_type, name='edit_ticket_type'),
    path('<uuid:event_pk>/delete-ticket-type/<uuid:ticket_type_pk>/',
         ticket_views.delete_ticket_type, name='delete_ticket_type'),
]

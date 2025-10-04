from django.urls import path
from .views import event_views, ticket_purchase_views, ticket_type_views, ticket_views

app_name = 'events'
urlpatterns = [
    # ----------------------  Event Views  ----------------------
    path('', event_views.events, name='events'),
    path('<uuid:pk>/', event_views.event_detail, name='event_detail'),
    path('<uuid:pk>/edit/', event_views.edit_event, name='edit_event'),
    path('new/', event_views.add_event, name='add_event'),
    path('<uuid:event_pk>/delete-event/',
         event_views.delete_event, name='delete_event'),

    # ----------------------  Ticket Type Views  ----------------------
    path('<uuid:event_pk>/add-ticket-type/',
         ticket_type_views.add_ticket_type, name='add_ticket_type'),
    path('<uuid:event_pk>/edit-ticket-type/<uuid:ticket_type_pk>/',
         ticket_type_views.edit_ticket_type, name='edit_ticket_type'),
    path('<uuid:event_pk>/delete-ticket-type/<uuid:ticket_type_pk>/',
         ticket_type_views.delete_ticket_type, name='delete_ticket_type'),

    # ---------------------  Ticket Pruchase Views  --------------------
    path('<uuid:event_pk>/purchase-ticket/<uuid:ticket_type_pk>/',
         ticket_purchase_views.buy_ticket, name='buy_ticket'),
    path('<uuid:event_pk>/confirm-ticket-purchase/<str:ticket_code>/',
         ticket_purchase_views.confirm_purchase, name='confirm_ticket_purchase'),
    path('<uuid:event_pk>/cancel-reservation/<str:ticket_code>/',
         ticket_purchase_views.cancel_reservation, name='cancel_reservation'),

    path('<uuid:event_pk>/ticket-purchase/success/<str:ticket_code>/',
         ticket_purchase_views.success_ticket_purchase, name='success_ticket_purchase'),
    path('<uuid:event_pk>/ticket-purchase/cancel/<str:ticket_code>/',
         ticket_purchase_views.cancel_ticket_purchase, name='cancel_ticket_purchase'),

    # ---------------------  Ticket Views  --------------------
    path('tickets/', ticket_views.tickets, name="tickets")

]

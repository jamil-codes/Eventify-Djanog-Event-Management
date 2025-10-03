import stripe
from django.urls import reverse
from .models import Ticket
from decouple import config

stripe.api_key = config("STRIPE_API_KEY", default=None)


def get_stripe_checkout_url(ticket: Ticket, success_url: str, cancel_url: str) -> str:
    # Create/retrieve Stripe Product
    if not ticket.stripe_product_id:
        product = stripe.Product.create(
            name=ticket.ticket_type.name,
            description=ticket.ticket_type.description,
        )
        ticket.stripe_product_id = product.id
        ticket.save(update_fields=['stripe_product_id'])
    else:
        product = stripe.Product.retrieve(ticket.stripe_product_id)

    # Create/retrieve Stripe Price
    if not ticket.stripe_price_id:
        price = stripe.Price.create(
            unit_amount=int(ticket.stripe_price),
            currency="usd",
            product=product.id,
        )
        ticket.stripe_price_id = price.id
        ticket.save(update_fields=['stripe_price_id'])
    else:
        price = stripe.Price.retrieve(ticket.stripe_price_id)

    # Create/retrieve Stripe Checkout Session
    if not ticket.stripe_session_id:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price': price.id, 'quantity': 1}],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "ticket_id": str(ticket.id),
                "user_id": str(ticket.attendee.id),
            }
        )
        ticket.stripe_session_id = session.id
        ticket.save(update_fields=['stripe_session_id'])
    else:
        session = stripe.checkout.Session.retrieve(ticket.stripe_session_id)

    return session.url

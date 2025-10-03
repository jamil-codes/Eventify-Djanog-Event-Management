# events/management/commands/fix_null_reservations.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from events.models import Ticket, PurchaseStatus


class Command(BaseCommand):
    help = "Fix or delete tickets with null reservation_expires_at"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete invalid tickets instead of fixing them",
        )
        parser.add_argument(
            "--minutes",
            type=int,
            default=15,
            help="Reservation window in minutes (default: 15)",
        )

    def handle(self, *args, **options):
        qs = Ticket.objects.filter(
            purchase_status=PurchaseStatus.PENDING,
            reservation_expires_at__isnull=True,
        )

        if options["delete"]:
            count, _ = qs.delete()
            self.stdout.write(
                self.style.WARNING(f"Deleted {count} tickets with null expiry")
            )
        else:
            now = timezone.now()
            count = qs.update(reservation_expires_at=now +
                              timedelta(minutes=options["minutes"]))
            self.stdout.write(
                self.style.SUCCESS(
                    f"Updated {count} tickets with new expiry (+{options['minutes']}m)")
            )

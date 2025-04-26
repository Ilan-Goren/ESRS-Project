"""
Management command to cleanup expired inventory items.

This command can be run periodically to archive or remove expired inventory items.
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.db import transaction
import datetime
import logging

from store.models import Inventory, Transaction, UserProfile
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command to cleanup expired inventory items."""
    
    help = 'Cleanup expired inventory items by marking them as archived/removed'
    
    def add_arguments(self, parser):
        """
        Add command arguments.
        
        Args:
            parser: The argument parser.
        """
        parser.add_argument(
            '--days',
            type=int,
            default=0,
            help='Include items expired more than this many days ago (default: 0 - today only)'
        )
        
        parser.add_argument(
            '--remove',
            action='store_true',
            help='Remove expired items from inventory (set quantity to 0)'
        )
        
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes'
        )
    
    def handle(self, *args, **options):
        """
        Handle the command execution.
        
        Args:
            *args: Command arguments.
            **options: Command options.
        """
        days = options['days']
        remove = options['remove']
        dry_run = options['dry_run']
        
        # Calculate the cutoff date
        today = timezone.now().date()
        cutoff_date = today - datetime.timedelta(days=days)
        
        # Get expired items
        expired_items = Inventory.objects.filter(
            expiry_date__lt=cutoff_date,
            quantity__gt=0  # Only items with quantity > 0
        )
        
        count = expired_items.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS(f"No expired items found before {cutoff_date}."))
            return
        
        self.stdout.write(f"Found {count} expired items before {cutoff_date}.")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No changes will be made."))
            
            for item in expired_items:
                self.stdout.write(
                    f"Would process: {item.item_name} (ID: {item.id}), "
                    f"Expired on: {item.expiry_date}, Quantity: {item.quantity}"
                )
            
            return
        
        # Get system user for logging transactions
        try:
            system_user = User.objects.get(username='system')
            system_profile = system_user.profile
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            # Create system user if it doesn't exist
            system_user = User.objects.create_user(
                username='system',
                email='system@example.com',
                password=User.objects.make_random_password()
            )
            system_profile = UserProfile.objects.create(
                user=system_user,
                role='admin'
            )
        
        # Process the expired items
        with transaction.atomic():
            for item in expired_items:
                original_quantity = item.quantity
                
                if remove:
                    # Create transaction record
                    Transaction.objects.create(
                        inventory=item,
                        user=system_profile,
                        quantity_used=original_quantity,
                        transaction_type='removed'
                    )
                    
                    # Set quantity to 0
                    item.quantity = 0
                    item.save()
                    
                    self.stdout.write(
                        f"Removed: {item.item_name} (ID: {item.id}), "
                        f"Expired on: {item.expiry_date}, Removed quantity: {original_quantity}"
                    )
                else:
                    self.stdout.write(
                        f"Found: {item.item_name} (ID: {item.id}), "
                        f"Expired on: {item.expiry_date}, Quantity: {original_quantity}"
                    )
        
        action = "Removed" if remove else "Found"
        self.stdout.write(self.style.SUCCESS(f"{action} {count} expired items."))
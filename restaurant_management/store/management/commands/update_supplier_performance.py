"""
Management command to update supplier performance metrics.

This command calculates and updates performance metrics for all suppliers.
It can be run periodically to maintain up-to-date supplier performance data.
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.db import transaction
import datetime
import logging

from store.models import Supplier, Order
from supplier.models import SupplierPerformance
from supplier.utils import calculate_supplier_metrics


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command to update supplier performance metrics."""
    
    help = 'Calculate and update performance metrics for all suppliers'
    
    def add_arguments(self, parser):
        """
        Add command arguments.
        
        Args:
            parser: The argument parser.
        """
        parser.add_argument(
            '--months',
            type=int,
            default=1,
            help='Number of months to calculate metrics for (default: 1)'
        )
        
        parser.add_argument(
            '--supplier-id',
            type=int,
            help='Calculate metrics only for this supplier ID'
        )
        
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recalculation even if metrics already exist'
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
        months = options['months']
        supplier_id = options['supplier_id']
        force = options['force']
        dry_run = options['dry_run']
        
        # Get the current date
        today = timezone.now().date()
        
        # Get suppliers
        if supplier_id:
            try:
                suppliers = [Supplier.objects.get(id=supplier_id)]
                self.stdout.write(f"Processing supplier with ID {supplier_id} only.")
            except Supplier.DoesNotExist:
                raise CommandError(f"Supplier with ID {supplier_id} does not exist.")
        else:
            suppliers = Supplier.objects.all()
            self.stdout.write(f"Processing all {suppliers.count()} suppliers.")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No changes will be made."))
        
        # Calculate metrics for each supplier and month
        for supplier in suppliers:
            self.stdout.write(f"Processing supplier: {supplier.name} (ID: {supplier.id})")
            
            for i in range(months):
                # Calculate month period
                month_end = today.replace(day=1) - datetime.timedelta(days=1) - datetime.timedelta(days=30*i)
                month_start = month_end.replace(day=1)
                
                self.stdout.write(f"  Calculating metrics for period: {month_start} to {month_end}")
                
                # Check if metrics already exist for this period
                existing_metrics = SupplierPerformance.objects.filter(
                    supplier=supplier,
                    period_start=month_start,
                    period_end=month_end
                ).first()
                
                if existing_metrics and not force:
                    self.stdout.write(f"  Metrics already exist for this period. Use --force to recalculate.")
                    continue
                
                # Calculate metrics
                metrics = calculate_supplier_metrics(supplier, month_start, month_end)
                
                if dry_run:
                    self.stdout.write(
                        f"  Would {'update' if existing_metrics else 'create'} metrics: "
                        f"Total Orders: {metrics['total_orders']}, "
                        f"On-Time: {metrics['on_time_deliveries']}, "
                        f"Late: {metrics['late_deliveries']}, "
                        f"On-Time %: {metrics['on_time_percentage']:.1f}%"
                    )
                else:
                    # Create or update performance record
                    with transaction.atomic():
                        if existing_metrics:
                            # Update existing record
                            existing_metrics.total_orders = metrics['total_orders']
                            existing_metrics.on_time_deliveries = metrics['on_time_deliveries']
                            existing_metrics.late_deliveries = metrics['late_deliveries']
                            existing_metrics.save()
                            
                            self.stdout.write(self.style.SUCCESS(f"  Updated existing metrics record."))
                        else:
                            # Create new record
                            performance = SupplierPerformance.objects.create(
                                supplier=supplier,
                                total_orders=metrics['total_orders'],
                                on_time_deliveries=metrics['on_time_deliveries'],
                                late_deliveries=metrics['late_deliveries'],
                                quality_rating=0.00,  # Default - can be manually updated later
                                period_start=month_start,
                                period_end=month_end
                            )
                            
                            self.stdout.write(self.style.SUCCESS(f"  Created new metrics record."))
        
        self.stdout.write(self.style.SUCCESS("Successfully updated supplier performance metrics."))
import csv
from datetime import datetime
import os
from django.core.management.base import BaseCommand
from django.db import transaction

from main.models import Child, Placement, Provider


def parse_date(date_str):
    """Utility to parse MM/DD/YY or MM/DD/YYYY dates safely."""
    if not date_str or date_str.strip() == "":
        return None
    date_str = date_str.strip()
    for fmt in ("%m/%d/%y", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass
    return None


def parse_int(val_str):
    """Utility to parse optional integers safely."""
    if not val_str or val_str.strip() == "":
        return None
    try:
        return int(float(val_str))
    except ValueError:
        return None


class Command(BaseCommand):
    help = "Import seed data from CSV files into PostgreSQL"

    def handle(self, *args, **options):
        # 1. Import Children First
        self.import_children(os.path.join("datadumps", "child_level.csv"))

        # 2. Import Providers
        self.import_providers(os.path.join("datadumps", "provider_level_updated.csv"))

        # 3. Import Placements Last (depends on Children & Providers)
        self.import_placements(os.path.join("datadumps", "placement_level.csv"))

    def import_children(self, filename):
        self.stdout.write("Importing Children...")
        try:
            with open(filename, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                objects = []
                for row in reader:
                    objects.append(
                        Child(
                            id_child=parse_int(row["id_child"]),
                            removal_date=parse_date(row["removal_date"]),
                            discharge_date=parse_date(row["discharge_date"]),
                            age_at_removal=parse_int(row["age_at_removal"]),
                            most_recent_age=parse_int(row["most_recent_age"]),
                            removal_county=row["removal_county"].strip(),
                        )
                    )

                with transaction.atomic():
                    Child.objects.bulk_create(
                        objects, ignore_conflicts=True, batch_size=2000
                    )
            self.stdout.write(self.style.SUCCESS(f"Imported {len(objects)} children."))
        except FileNotFoundError:
            self.stderr.write(f"File {filename} not found.")

    def import_providers(self, filename):
        self.stdout.write("Importing Providers...")
        try:
            with open(filename, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                objects = []
                for row in reader:
                    objects.append(
                        Provider(
                            id_provider=parse_int(row["id_provider"]),
                            license_start_date=parse_date(row["license_start_date"]),
                            license_end_date=parse_date(row["license_end_date"]),
                            county_provider=row["county_provider"].strip(),
                            n_days_licensed=parse_int(row["n_days_licensed"]),
                            n_days_active=parse_int(row["n_days_active"]),
                            min_age=parse_int(row["min_age"]),
                            max_age=parse_int(row["max_age"]),
                        )
                    )

                with transaction.atomic():
                    Provider.objects.bulk_create(
                        objects, ignore_conflicts=True, batch_size=2000
                    )
            self.stdout.write(self.style.SUCCESS(f"Imported {len(objects)} providers."))
        except FileNotFoundError:
            self.stderr.write(f"File {filename} not found.")

    def import_placements(self, filename):
        self.stdout.write("Importing Placements...")
        try:
            # Cache valid FK IDs to prevent database lookup overhead during bulk build
            valid_child_ids = set(Child.objects.values_list("id_child", flat=True))
            valid_provider_ids = set(
                Provider.objects.values_list("id_provider", flat=True)
            )

            with open(filename, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                objects = []
                for row in reader:
                    child_id = parse_int(row["id_child"])
                    provider_id = parse_int(row["id_provider"])

                    # Ensure child FK exists in DB
                    if child_id not in valid_child_ids:
                        continue

                    # Ensure provider FK exists in DB or assign None
                    if provider_id not in valid_provider_ids:
                        provider_id = None

                    objects.append(
                        Placement(
                            child_id=child_id,
                            provider_id=provider_id,
                            placement_start_date=parse_date(
                                row["placement_start_date"]
                            ),
                            placement_end_date=parse_date(row["placement_end_date"]),
                            resource_type_on_this_placement=row[
                                "resource_type_on_this_placement"
                            ].strip(),
                            placement_index=parse_int(row["placement_index"]),
                            removal_county=row["removal_county"].strip(),
                            placement_county=row["placement_county"].strip(),
                            placement_length=parse_int(row["placement_length"]),
                        )
                    )

                with transaction.atomic():
                    Placement.objects.bulk_create(
                        objects, ignore_conflicts=True, batch_size=2000
                    )
            self.stdout.write(
                self.style.SUCCESS(f"Imported {len(objects)} placements.")
            )
        except FileNotFoundError:
            self.stderr.write(f"File {filename} not found.")

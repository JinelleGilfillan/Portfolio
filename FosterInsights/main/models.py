from django.db import models


class Child(models.Model):
    id_child = models.IntegerField(primary_key=True)
    removal_date = models.DateField()
    discharge_date = models.DateField(null=True, blank=True)
    age_at_removal = models.IntegerField(null=True, blank=True)
    most_recent_age = models.IntegerField(null=True, blank=True)
    removal_county = models.CharField(max_length=100)

    def __str__(self):
        return f"Child {self.id_child}"


class Provider(models.Model):
    id_provider = models.IntegerField(primary_key=True)
    license_start_date = models.DateField()
    license_end_date = models.DateField()
    county_provider = models.CharField(max_length=100)
    n_days_licensed = models.IntegerField()
    n_days_active = models.IntegerField()
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    def __str__(self):
        return f"Provider {self.id_provider}"


class Placement(models.Model):
    child = models.ForeignKey(
        Child, on_delete=models.CASCADE, related_name="placements"
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="placements",
    )
    placement_start_date = models.DateField()
    placement_end_date = models.DateField()
    resource_type_on_this_placement = models.CharField(max_length=100)
    placement_index = models.IntegerField()
    removal_county = models.CharField(max_length=100)
    placement_county = models.CharField(max_length=100)
    placement_length = models.IntegerField()

    def __str__(self):
        return f"Placement {self.placement_index} for Child {self.child_id}"

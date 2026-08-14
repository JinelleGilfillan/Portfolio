from django.urls import path

from api.views import (
    my_protected_endpoint,
    child_provider_stats,
    out_of_county_placements,
)

urlpatterns = [
    path("my-protected-endpoint/", my_protected_endpoint, name="my_protected"),
    path("child-provider-stats/", child_provider_stats, name="child_provider_stats"),
    path(
        "out-of-county-placements/",
        out_of_county_placements,
        name="out_of_county_placements",
    ),
]

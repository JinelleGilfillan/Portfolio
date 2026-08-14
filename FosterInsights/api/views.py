import datetime

from django.db.models import Case, CharField, Count, OuterRef, Subquery, Value, When, F
from django.db.models.functions import ExtractYear
from rest_framework.decorators import api_view
from rest_framework.response import Response

from main.core_security import protected_api_view
from main.models import Child, Placement, Provider

# Define standard age groups
AGE_GROUPS = [
    {"label": "0-2", "min": 0, "max": 2},
    {"label": "3-5", "min": 3, "max": 5},
    {"label": "6-9", "min": 6, "max": 9},
    {"label": "10-14", "min": 10, "max": 14},
    {"label": "15-18", "min": 15, "max": 18},
]


@api_view(["GET"])
@protected_api_view
def my_protected_endpoint(request):
    return Response({"status": "success", "message": "Authenticated & Verified!"})


@api_view(["GET"])
@protected_api_view
def child_provider_stats(request):
    latest_placement_type = (
        Placement.objects.filter(child=OuterRef("pk"))
        .order_by("-placement_start_date")
        .values("resource_type_on_this_placement")[:1]
    )

    active_children = (
        Child.objects.filter(discharge_date__isnull=True)
        .annotate(current_resource_type=Subquery(latest_placement_type))
        .exclude(
            current_resource_type="kin"
        )  # exclue children currently placed with kin as capacity demand
    )

    active_providers = Provider.objects.filter(
        license_end_date__gte=datetime.date(2026, 7, 1)
    )

    child_counties = active_children.values_list("removal_county", flat=True).distinct()
    provider_counties = active_providers.values_list(
        "county_provider", flat=True
    ).distinct()
    all_counties = sorted(list(set(child_counties) | set(provider_counties)))

    response_data = []
    for county in all_counties:
        county_children = active_children.filter(removal_county=county)
        county_providers_qs = active_providers.filter(county_provider=county)

        pools = {g["label"]: [] for g in AGE_GROUPS}

        for p in county_providers_qs:
            is_at_risk = p.n_days_licensed >= 180 and p.n_days_active < (
                p.n_days_licensed * 0.20
            )
            p_obj = {
                "id": p.id_provider,
                "min_age": p.min_age,
                "max_age": p.max_age,
                "is_at_risk": is_at_risk,
            }

            # Put in highest fitting bucket
            if p.max_age >= 15:
                pools["15-18"].append(p_obj)
            elif p.max_age >= 10:
                pools["10-14"].append(p_obj)
            elif p.max_age >= 6:
                pools["6-9"].append(p_obj)
            elif p.max_age >= 3:
                pools["3-5"].append(p_obj)
            else:
                pools["0-2"].append(p_obj)

        # Process from top down to allow surplus to trickle
        for group in AGE_GROUPS:
            label = group["label"]
            county_age_children = county_children.filter(
                most_recent_age__gte=group["min"], most_recent_age__lte=group["max"]
            )
            child_count = county_age_children.count()
            non_family_count = county_age_children.filter(
                current_resource_type="nonfamily"
            ).count()

            current_provider_count = len(pools[label])

            # If current bracket has a deficit (childCount > providerCount)
            deficit = child_count - current_provider_count

            if deficit > 0:
                # Look at higher groups to see if any have SURPLUS providers
                for higher_group in AGE_GROUPS:
                    if higher_group["min"] <= group["min"]:
                        continue  # Only look at strictly higher brackets

                    higher_label = higher_group["label"]
                    higher_children = county_children.filter(
                        most_recent_age__gte=higher_group["min"],
                        most_recent_age__lte=higher_group["max"],
                    ).count()

                    higher_pool = pools[higher_label]

                    # Surplus ONLY exists if providers > children in that higher group
                    surplus = len(higher_pool) - higher_children

                    if surplus > 0:
                        # Find providers in higher pool who can legally take kids in this lower group
                        candidates = [
                            p for p in higher_pool if p["min_age"] <= group["max"]
                        ]

                        num_to_move = min(deficit, surplus, len(candidates))

                        for i in range(num_to_move):
                            p_to_move = candidates[i]
                            higher_pool.remove(p_to_move)
                            pools[label].append(p_to_move)
                            deficit -= 1
                            if deficit <= 0:
                                break

                    if deficit <= 0:
                        break

        county_results = []
        for group in reversed(AGE_GROUPS):
            label = group["label"]
            county_age_children = county_children.filter(
                most_recent_age__gte=group["min"], most_recent_age__lte=group["max"]
            )
            child_count = county_age_children.count()
            non_family_count = county_age_children.filter(
                current_resource_type="nonfamily"
            ).count()

            final_pool = pools[label]
            county_results.append(
                {
                    "county": county,
                    "ageGroup": label,
                    "childCount": child_count,
                    "providerCount": len(final_pool),
                    "atRiskProviderCount": sum(
                        1 for p in final_pool if p["is_at_risk"]
                    ),
                    "nonFamilyCount": non_family_count,
                }
            )

        response_data.extend(county_results)

    return Response(response_data)


@api_view(["GET"])
@protected_api_view
def out_of_county_placements(request):
    # 1. Subqueries to pull the latest placement's resource type and provider county
    latest_placement = Placement.objects.filter(child=OuterRef("pk")).order_by(
        "-placement_start_date"
    )

    latest_placement_type = latest_placement.values("resource_type_on_this_placement")[
        :1
    ]
    latest_placement_county = latest_placement.values("provider__county_provider")[:1]

    # 2. Filter active out-of-county children & aggregate counts
    out_of_county_data = (
        Child.objects.filter(discharge_date__isnull=True)
        .annotate(
            current_resource_type=Subquery(latest_placement_type),
            placement_county=Subquery(latest_placement_county),
        )
        .exclude(current_resource_type="kin")
        # Ensure we only include valid out-of-county placements
        .filter(placement_county__isnull=False)
        .exclude(placement_county=F("removal_county"))
        # Group by removal and placement county
        .values(
            removalCounty=F("removal_county"),
            placementCounty=F("placement_county"),
        )
        .annotate(childCount=Count("id_child"))
        .order_by("removalCounty", "placementCounty")
    )

    return Response(list(out_of_county_data))

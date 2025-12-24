import csv
import os
from os import error

from django.conf import settings
from .models import Country, State, Industry, AnnualIncome


def clean_rate(rate):
    """Convert rate string like '$93,485' to positive integer"""
    rate_str = str(rate).replace("$", "").replace(",", "").strip()
    if rate_str == "":
        return None
    try:
        rate_int = int(float(rate_str))  # Convert to float first, then int
        return rate_int if rate_int >= 0 else None  # Ensure positive
    except (ValueError, TypeError):
        return None


def tax_records():
    csv_path = os.path.join(settings.BASE_DIR, 'require', 'income_records.csv')

    # Get or create country
    country_name = "United States"
    country, created = Country.objects.get_or_create(
        name=country_name,
        defaults={
            "short_name": "US",
            "language": "en",
            "currency": "USD",
            "phone_code": "+1",
            "is_services_available": True,
            "is_active": True,
        }
    )
    if created:
        print(f"Created country: {country_name}")

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    states = rows[0][1:]  # Skip 'Industry' column

    # Create/get all states
    state_objs = {}
    for state_name in states:
        state_obj, created = State.objects.get_or_create(
            name=state_name.strip(),
            country=country,
            defaults={"is_active": True}
        )
        state_objs[state_name] = state_obj
        if created:
            print(f"Created state: {state_name}")

    # Create/get all industries, then import taxes
    for row in rows[1:]:
        industry_name = row[0].strip()
        industry_obj, created = Industry.objects.get_or_create(
            name=industry_name,
            defaults={"is_active": True}
        )
        if created:
            print(f"Created industry: {industry_name}")

        for i, rate in enumerate(row[1:]):
            state_name = states[i].strip()
            state_obj = state_objs[state_name]
            rate_int = clean_rate(rate)

            if rate_int is None:
                print(f"Skipping invalid rate for {industry_name} in {state_name}: {rate}")
                continue

            # Find or create Tax record
            annual_income, created = AnnualIncome.objects.get_or_create(
                state=state_obj,
                industry=industry_obj,
                defaults={"rate": rate_int, "is_active": True}
            )

            if not created:
                if annual_income.rate != rate_int:
                    annual_income.rate = rate_int
                    annual_income.save()
                    print(f"Updated Annual Income: {annual_income.name} to rate {annual_income.rate}")
                # Removed the "already up to date" message to reduce output
            else:
                print(f"Created Annual Income: {annual_income.name} with rate {annual_income.rate}")

    print("Annual Income import completed successfully!")


def log_error(object_id, object_name, error_message, data=None, is_external=True):
    from .models import ErrorLog
    try:
        obj, created = ErrorLog.objects.get_or_create(
            object_id=object_id,
            object_name=object_name,
            error_message=error_message,
            data=data,
            is_external=is_external
        )
        print(
            f"\n"
            f"----------------------------------------------------------------\n"
            f"  ERROR LOG | CREATED :{created} > OBJECT {object_name} (ID: {object_id})\n"
            f"----------------------------------------------------------------\n"
            f"\n"
        )
    except error as e:
        pass

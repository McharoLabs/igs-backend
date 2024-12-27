from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from decimal import Decimal

def calculate_checkout_date(amount: Decimal, price_per_month: Decimal) -> str:
    """
    Calculates the check-out date based on the amount paid and the monthly price.

    Args:
    - amount: The total amount paid by the tenant (or any other entity). This can be a string or Decimal.
    - price_per_month: The cost per month (could be for rent, service, etc.).

    Returns:
    - A string representing the check-out date.
    """
    if price_per_month <= 0:
        raise ValueError("Price per month must be greater than zero.")

    if isinstance(amount, str):
        try:
            amount = Decimal(amount)
        except ValueError:
            raise ValueError("Invalid amount format, must be a number.")

    months = int(amount / price_per_month)
    
    if months <= 0:
        raise ValueError("The amount must be sufficient for at least one month.")

    check_in_date = timezone.now().date()

    check_out_date = check_in_date + relativedelta(months=months)

    return str(check_out_date) 

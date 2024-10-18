import random
import string

from django.core.paginator import Paginator
from django.db.models import Max
from django.utils import timezone


def generate_unique_id(size=8, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def generate_order_id(auto_id=""):
    today = timezone.now()
    return (
        str(today.year)
        + str(today.day).zfill(2)
        + str(today.month).zfill(2)
        + str(today.strftime("%I%M%s"))
    )


def generate_form_errors(args, formset=False):
    message = ""
    if not formset:
        for field in args:
            if field.errors:
                message += field.label + " : "
                error = field.errors[0]
                message += str(error)
                message += "\n"

        for err in args.non_field_errors():
            error = err
            message += str(error)
            message += "\n"
    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    message += field.label + " : "
                    error = field.errors[0]
                    message += str(error)
                    message += "\n"
            for err in form.non_field_errors():
                error = err
                message += str(error)
                message += "\n"

    return message


def get_auto_id(model):
    if model.objects.exists():
        latest_auto_id = model.objects.aggregate(max_auto_id=Max("auto_id")).get(
            "max_auto_id", 0
        )
        auto_id = int(latest_auto_id) + 1
    else:
        auto_id = 1

    return auto_id


def random_string():
    return f"{string.ascii_letters}{string.digits}"


def get_country_code(country):
    country_code = "5" if country == "uae" else "10"

    return country_code


def has_key_startswith(key, dict_data):
    """
    Usage:
    >>> has_key_startswith('user', {'user__iexact': 'abcd'})
    >>> True
    """
    for _key, _values in dict_data.items():
        if len(_values) == 0:
            continue
        if _key.startswith(key):
            return True
    return False


def paginate(instances, request):
    paginator = Paginator(instances, 9)
    page_number = request.GET.get("page")
    instances = paginator.get_page(page_number)
    return instances


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

import re
from django.utils.html import format_html
from django.utils.safestring import mark_safe


def send_email(subject, message, recipient_list, from_email=None, fail_silently=False, connection=None, html_message=None, attachments=None):
    from django.core.mail import EmailMultiAlternatives

    email = EmailMultiAlternatives(subject, message, from_email, recipient_list, connection=connection)
    email.attach_alternative(html_message, "text/html")
    if attachments:
        for attachment in attachments:
            email.attach_file(attachment)
    return email.send(fail_silently=fail_silently)


def get_value(model, pk, default=None):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return default


def auto_linkify_urls(value):
    url_regex = r"(https?://\S+)"
    return re.sub(url_regex, r'<a href="\1">\1</a>', value)


def generate_value(self, field):
    class_type = field.__class__.__name__

    if class_type in ("ForeignKey", "OneToOneField"):
        model = field.related_model
        try:
            value = get_value(model, field.value_from_object(self))
            return format_html('<a href="{}">{}</a>', value.get_absolute_url(), value)
        except (model.DoesNotExist, AttributeError):
            return field.value_from_object(self)

    elif class_type == "ManyToManyField":
        model = field.related_model
        values = [get_value(model, pk) for pk in field.value_from_object(self)]
        return ", ".join(str(value) for value in values)

    elif class_type == "CharField" and field.verbose_name.title() == "Password":
        return "- - encrypted - -"

    elif class_type in ("ImageField", "VersatileImageField", "ThumbnailerImageField"):
        media_url = "/media/"
        field_value = field.value_from_object(self)
        if field_value:
            return format_html('<a href="{}{}" target="_blank">Open Image</a>', media_url, field_value)
        else:
            return "-"

    elif class_type == "FileField":
        media_url = "/media/"
        field_value = field.value_from_object(self)
        if field_value:
            return format_html('<a href="{}{}" target="_blank">Open File</a>', media_url, field_value)
        else:
            return "-"

    elif class_type == "CurrencyField":
        return None

    elif class_type == "HTMLField":
        field_value = field.value_from_object(self)
        if field_value:
            return format_html(field_value)
        else:
            return "-"

    elif class_type == "TextField":
        field_value = field.value_from_object(self)
        if field_value:
            linked_value = auto_linkify_urls(field_value)
            formatted_value = "<br>".join(linked_value.splitlines())
            return format_html(mark_safe(formatted_value))
        else:
            return "-"

    else:
        return field.value_from_object(self)


def generate_fields(self):
    return [(field.verbose_name.title(), generate_value(self, field)) for field in self._meta.fields]




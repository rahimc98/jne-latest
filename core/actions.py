from django.contrib import messages
from django.utils.translation import ngettext


def mark_inactive(self, request, queryset):
    updated = queryset.update(is_active=False)
    self.message_user(request, ngettext("%d item was successfully marked as deleted.", "%d items were successfully marked as deleted.", updated) % updated, messages.SUCCESS)


def mark_active(self, request, queryset):
    updated = queryset.update(is_active=True)
    self.message_user(request, ngettext("%d item was successfully marked as active.", "%d items were successfully marked as active.", updated) % updated, messages.SUCCESS)

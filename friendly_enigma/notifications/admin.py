from django.contrib.admin import ModelAdmin, site
from django import forms
from .models import Notification


class NotificationAdmin(ModelAdmin):
    raw_id_fields = ("recipient",)
    list_display = ("recipient", "type", "text", "is_read")
    list_filter = (
        "is_read",
        "timestamp",
    )

    def get_form(self, request, obj=None, **kwargs):
        kwargs["widgets"] = {"text": forms.Textarea}
        return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(NotificationAdmin, self).get_queryset(request)
        return qs.prefetch_related("actor")


site.register(Notification, NotificationAdmin)

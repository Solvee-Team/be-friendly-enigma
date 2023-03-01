from django.utils.timezone import now

from user.models import User


class SetLastVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.user.is_authenticated:
            # Update last login time after request finished processing.
            # in future we need to change this to last visit
            User.objects.filter(pk=request.user.pk).update(last_visit=now())

        response = self.get_response(request)
        return response

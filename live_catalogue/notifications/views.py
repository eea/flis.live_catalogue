from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from braces.views import JSONResponseMixin

from notifications.models import NotificationUser
from live_catalogue.auth import login_required, edit_permission_required


class Notifications(View):

    @method_decorator(login_required)
    @method_decorator(edit_permission_required)
    def get(self, request):
        try:
            notification_user = NotificationUser.objects.get(
                user_id=request.user_id)
        except NotificationUser.DoesNotExist:
            notification_user = None
        return render(request, 'notifications.html', {
            'notification_user': notification_user,
        })


class Subscribe(JSONResponseMixin, View):

    @method_decorator(login_required)
    @method_decorator(edit_permission_required)
    def post(self, request):
        NotificationUser.objects.get_or_create(user_id=request.user_id)
        url = reverse('notifications:home')
        data = {'status': 'success', 'url': url}
        return self.render_json_response(data)

    @method_decorator(login_required)
    @method_decorator(edit_permission_required)
    def delete(self, request):
        notifications_user = get_object_or_404(NotificationUser,
                                               user_id=request.user_id)
        notifications_user.delete()
        url = reverse('notifications:home')
        data = {'status': 'success', 'url': url}
        return self.render_json_response(data)

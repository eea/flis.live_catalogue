from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from braces.views import JSONResponseMixin

from notifications.models import NotificationUser
from live_catalogue.auth import PermissionRequiredMixin
from live_catalogue.definitions import (
    EDIT_ROLES,
    EDIT_GROUPS,
    ADMIN_ROLES, ADMIN_GROUPS)


class Notifications(PermissionRequiredMixin,
                    View):
    roles_required = EDIT_ROLES
    groups_required = EDIT_GROUPS

    def get(self, request):
        try:
            notification_user = NotificationUser.objects.get(
                user_id=self.user_id(request))
        except NotificationUser.DoesNotExist:
            notification_user = None
        return render(request, 'notifications.html', {
            'notification_user': notification_user,
        })


class Subscribe(PermissionRequiredMixin, JSONResponseMixin, View):
    roles_required = EDIT_ROLES
    groups_required = EDIT_GROUPS

    def post(self, request):
        notification_user, new = NotificationUser.objects.get_or_create(
            user_id=self.user_id(request))
        notification_user.subscribed = True
        notification_user.save()
        url = reverse('notifications:home')
        data = {'status': 'success', 'url': url}
        return self.render_json_response(data)

    def delete(self, request):
        notifications_user = get_object_or_404(NotificationUser,
                                               user_id=self.user_id(request))
        notifications_user.subscribed = False
        notifications_user.save()
        url = reverse('notifications:home')
        data = {'status': 'success', 'url': url}
        return self.render_json_response(data)


class NotificationsManager(PermissionRequiredMixin, View):
    roles_required = ADMIN_ROLES
    groups_required = ADMIN_GROUPS

    def get(self, request):
        users =  NotificationUser.objects.order_by('user_id')
        return render(request, 'notifications_manager.html', {
            'notification_users': users,
        })

from rest_framework.permissions import BasePermission
from organizations.models import Membership


class IsTaskActor(BasePermission):
    def has_object_permission(self, request, view, obj):
        membership = Membership.objects.filter(
            user=request.user,
            organization=obj.project.organization
        ).first()

        if not membership:
            return False

        if membership.role in [Membership.ROLE_OWNER, Membership.ROLE_ADMIN]:
            return True

        return obj.assigned_to == request.user

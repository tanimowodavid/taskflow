from rest_framework.permissions import BasePermission
from .models import Membership


class IsOrgAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        org_id = request.data.get("organization") or request.query_params.get("organization")
        if not org_id:
            return False

        return Membership.objects.filter(
            user=request.user,
            organization_id=org_id,
            role__in=[Membership.ROLE_OWNER, Membership.ROLE_ADMIN]
        ).exists()


# Only owners or admins can send invites
class IsOrgAdminOrOwnerFromOrg(BasePermission):
    def has_permission(self, request, view):
        org_id = request.data.get("organization")
        if not org_id:
            return False

        return Membership.objects.filter(
            user=request.user,
            organization_id=org_id,
            role__in=[Membership.ROLE_OWNER, Membership.ROLE_ADMIN]
        ).exists()

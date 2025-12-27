from rest_framework import generics, permissions
from .models import Organization, Membership, OrganizationInvite
from .serializers import OrganizationSerializer
from activity.utils import log_activity
from .serializers_invite import InviteCreateSerializer
from .permissions import IsOrgAdminOrOwnerFromOrg
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class OrganizationListCreateView(generics.ListCreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.filter(
            memberships__user=self.request.user
        )

    def perform_create(self, serializer):
        organization = serializer.save(owner=self.request.user)
        Membership.objects.create(
            user=self.request.user,
            organization=organization,
            role=Membership.ROLE_OWNER
        )

# Log organization creation

def perform_create(self, serializer):
    organization = serializer.save(owner=self.request.user)
    Membership.objects.create(
        user=self.request.user,
        organization=organization,
        role=Membership.ROLE_OWNER
    )
    log_activity(
        organization=organization,
        actor=self.request.user,
        action="Created organization"
    )


# Send invite
class InviteCreateView(generics.CreateAPIView):
    serializer_class = InviteCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgAdminOrOwnerFromOrg]

    def perform_create(self, serializer):
        invite = serializer.save(invited_by=self.request.user)
        log_activity(
            organization=invite.organization,
            actor=self.request.user,
            action=f"Invited {invite.email} to organization"
        )

# Accept invite

class AcceptInviteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, token):
        try:
            invite = OrganizationInvite.objects.get(token=token, is_accepted=False)
        except OrganizationInvite.DoesNotExist:
            raise ValidationError("Invalid invite")

        if invite.is_expired():
            raise ValidationError("Invite expired")

        if request.user.email != invite.email:
            raise ValidationError("Invite email mismatch")

        Membership.objects.create(
            user=request.user,
            organization=invite.organization,
            role=invite.role
        )

        invite.is_accepted = True
        invite.save()

        log_activity(
            organization=invite.organization,
            actor=request.user,
            action="Accepted organization invite"
        )

        return Response({"detail": "Invite accepted"})

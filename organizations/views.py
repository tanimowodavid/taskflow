from rest_framework import generics, permissions
from .models import Organization, Membership
from .serializers import OrganizationSerializer


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

from rest_framework import generics, permissions
from .models import Project
from .serializers import ProjectSerializer
from organizations.models import Membership
from organizations.permissions import IsOrgAdminOrOwner
from activity.utils import log_activity


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(
            organization__memberships__user=self.request.user
        )

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsOrgAdminOrOwner()]
        return super().get_permissions()


# Log project creation

def perform_create(self, serializer):
    project = serializer.save()
    log_activity(
        organization=project.organization,
        actor=self.request.user,
        action=f"Created project '{project.name}'"
    )

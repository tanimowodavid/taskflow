from rest_framework import generics, permissions
from .models import Project
from .serializers import ProjectSerializer
from organizations.models import Membership
from organizations.permissions import IsOrgAdminOrOwner


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

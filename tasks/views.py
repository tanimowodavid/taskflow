from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsTaskActor
from organizations.models import Membership


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            project__organization__memberships__user=self.request.user
        )

    def perform_create(self, serializer):
        membership = Membership.objects.get(
            user=self.request.user,
            organization=serializer.validated_data["project"].organization
        )

        if membership.role not in [Membership.ROLE_OWNER, Membership.ROLE_ADMIN]:
            raise permissions.PermissionDenied("Not allowed to create tasks")

        serializer.save()


class TaskDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskActor]

    def get_queryset(self):
        return Task.objects.filter(
            project__organization__memberships__user=self.request.user
        )

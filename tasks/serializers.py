from rest_framework import serializers
from .models import Task
from organizations.models import Membership


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "project",
            "title",
            "description",
            "assigned_to",
            "status",
            "priority",
            "due_date",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):
        request = self.context["request"]
        project = attrs.get("project")
        assigned_to = attrs.get("assigned_to")

        # Ensure user belongs to org
        if not Membership.objects.filter(
            user=request.user,
            organization=project.organization
        ).exists():
            raise serializers.ValidationError("Not a member of this organization")

        # Ensure assignee belongs to same org
        if assigned_to and not Membership.objects.filter(
            user=assigned_to,
            organization=project.organization
        ).exists():
            raise serializers.ValidationError("Assignee not in organization")

        return attrs

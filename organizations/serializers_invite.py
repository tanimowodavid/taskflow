from rest_framework import serializers
from .models import OrganizationInvite, Membership


class InviteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationInvite
        fields = ("organization", "email", "role")

    def validate(self, attrs):
        org = attrs["organization"]
        email = attrs["email"]

        if Membership.objects.filter(
            organization=org,
            user__email=email
        ).exists():
            raise serializers.ValidationError("User already in organization")

        return attrs

from django.test import TestCase
from common.tests import APITestBase
from organizations.models import Organization, Membership


class ProjectPermissionTests(TestCase, APITestBase):
    def test_member_cannot_create_project(self):
        owner = self.create_user("owner@test.com")
        member = self.create_user("member@test.com")

        org = Organization.objects.create(name="Org", owner=owner)
        Membership.objects.create(user=owner, organization=org, role="owner")
        Membership.objects.create(user=member, organization=org, role="member")

        client = self.authenticate(member)

        res = client.post(
            "/api/v1/projects/",
            {
                "name": "Forbidden Project",
                "organization": org.id,
            },
            format="json",
        )
        self.assertEqual(res.status_code, 403)

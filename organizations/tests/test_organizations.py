from django.test import TestCase
from common.tests import APITestBase
from organizations.models import Membership


class OrganizationTests(TestCase, APITestBase):
    def test_owner_membership_created(self):
        user = self.create_user()
        client = self.authenticate(user)

        res = client.post(
            "/api/v1/organizations/",
            {"name": "Test Org"},
            format="json",
        )
        self.assertEqual(res.status_code, 201)

        membership = Membership.objects.get(user=user)
        self.assertEqual(membership.role, Membership.ROLE_OWNER)

from types import SimpleNamespace

from django.test import SimpleTestCase

from profiles_api.permissions import UpdateOwnProfile


class UpdateOwnProfileTests(SimpleTestCase):
    def setUp(self):
        self.permission = UpdateOwnProfile()

    def test_unauthenticated_user_is_denied(self):
        request = SimpleNamespace(
            user=SimpleNamespace(is_authenticated=False)
        )
        self.assertFalse(self.permission.has_permission(request, None))

    def test_authenticated_user_is_allowed_to_reach_profile_endpoint(self):
        request = SimpleNamespace(
            user=SimpleNamespace(is_authenticated=True)
        )
        self.assertTrue(self.permission.has_permission(request, None))

    def test_safe_method_allows_read_access(self):
        request = SimpleNamespace(
            method="GET",
            user=SimpleNamespace(id=7, is_authenticated=True),
        )
        profile = SimpleNamespace(id=12)
        self.assertTrue(
            self.permission.has_object_permission(request, None, profile)
        )

    def test_owner_can_modify_own_profile(self):
        request = SimpleNamespace(
            method="PATCH",
            user=SimpleNamespace(id=7, is_authenticated=True),
        )
        profile = SimpleNamespace(id=7)
        self.assertTrue(
            self.permission.has_object_permission(request, None, profile)
        )

    def test_user_cannot_modify_another_profile(self):
        request = SimpleNamespace(
            method="PUT",
            user=SimpleNamespace(id=7, is_authenticated=True),
        )
        profile = SimpleNamespace(id=12)
        self.assertFalse(
            self.permission.has_object_permission(request, None, profile)
        )

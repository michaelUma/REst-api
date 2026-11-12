from rest_framework import status
from rest_framework.test import APITestCase

from .models import UserProfile


class UserProfileAccessTests(APITestCase):
    profile_list_url = '/api/profile/'

    def setUp(self):
        self.owner = UserProfile.objects.create_user(
            email='owner@example.com',
            name='Owner',
            password='OwnerPassword123!',
        )
        self.other = UserProfile.objects.create_user(
            email='other@example.com',
            name='Other',
            password='OtherPassword123!',
        )
        self.client.force_authenticate(user=self.owner)

    def profile_detail_url(self, user):
        return '{}{}/'.format(self.profile_list_url, user.pk)

    def test_unauthenticated_user_cannot_list_profiles(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.profile_list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_returns_only_authenticated_users_profile(self):
        response = self.client.get(self.profile_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [profile['id'] for profile in response.data],
            [self.owner.pk],
        )
        self.assertNotIn('password', response.data[0])

    def test_owner_can_retrieve_own_profile(self):
        response = self.client.get(self.profile_detail_url(self.owner))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.owner.pk)

    def test_user_cannot_retrieve_another_profile(self):
        response = self.client.get(self.profile_detail_url(self.other))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_update_own_profile(self):
        response = self.client.patch(
            self.profile_detail_url(self.owner),
            {'name': 'Updated Owner'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.name, 'Updated Owner')

    def test_user_cannot_update_another_profile(self):
        response = self.client.patch(
            self.profile_detail_url(self.other),
            {'name': 'Changed'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.other.refresh_from_db()
        self.assertEqual(self.other.name, 'Other')

    def test_password_updates_are_hashed(self):
        new_password = 'NewSecurePassword123!'

        response = self.client.patch(
            self.profile_detail_url(self.owner),
            {'password': new_password},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', response.data)
        self.owner.refresh_from_db()
        self.assertTrue(self.owner.check_password(new_password))

from django.test import TestCase, RequestFactory
from users.models import User
from users.permissions import IsSelfOrReadOnly


class IsSelfOrReadOnlyTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='testpass123'
        )
        self.permission = IsSelfOrReadOnly()

    def test_safe_methods_allowed(self):
        """Проверяет, что безопасные методы разрешены для всех"""
        safe_methods = ['GET', 'HEAD', 'OPTIONS']

        for method in safe_methods:
            request = self.factory.generic(method, '/')
            request.user = self.user1

            self.assertTrue(
                self.permission.has_object_permission(request, None, self.user1)
            )

            self.assertTrue(
                self.permission.has_object_permission(request, None, self.user2)
            )

    def test_unsafe_methods_self(self):
        """Проверяет, что небезопасные методы разрешены только для своего профиля"""
        unsafe_methods = ['PUT', 'PATCH', 'DELETE']

        for method in unsafe_methods:
            request = self.factory.generic(method, '/')
            request.user = self.user1

            self.assertTrue(
                self.permission.has_object_permission(request, None, self.user1)
            )

            self.assertFalse(
                self.permission.has_object_permission(request, None, self.user2)
            )

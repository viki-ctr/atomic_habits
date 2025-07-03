from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.serializers import HabitSerializer
from users.models import User


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Пить кофе",
            is_pleasant=True,
            duration=60
        )

    def test_habit_creation(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Парк",
            time="09:00:00",
            action="Гулять",
            duration=120,
            related_habit=self.pleasant_habit
        )
        self.assertEqual(habit.action, "Гулять")
        self.assertEqual(habit.related_habit, self.pleasant_habit)

    def test_invalid_duration(self):
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                place="Офис",
                time="10:00:00",
                action="Работать",
                duration=121
            )
            habit.full_clean()

    def test_invalid_related_habit(self):
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                place="Офис",
                time="10:00:00",
                action="Работать",
                duration=60,
                related_habit=self.pleasant_habit,
                reward="Кофе"
            )
            habit.full_clean()


class HabitSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.habit_data = {
            'place': 'Дом',
            'time': '08:00:00',
            'action': 'Пить воду',
            'duration': 60,
            'is_public': True
        }

    def test_valid_serializer(self):
        serializer = HabitSerializer(
            data=self.habit_data,
            context={'request': type('obj', (object,), {'user': self.user})}
        )
        self.assertTrue(serializer.is_valid())

    def test_invalid_duration(self):
        invalid_data = self.habit_data.copy()
        invalid_data['duration'] = 121
        serializer = HabitSerializer(
            data=invalid_data,
            context={'request': type('obj', (object,), {'user': self.user})}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('duration', serializer.errors)


class HabitViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Пить воду",
            duration=60
        )

    def test_list_habits(self):
        url = reverse('habits-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_habit(self):
        url = reverse('habits-list')
        data = {
            'place': 'Офис',
            'time': '10:00:00',
            'action': 'Работать',
            'duration': 90
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_retrieve_habit(self):
        url = reverse('habits-detail', args=[self.habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'Пить воду')

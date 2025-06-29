from rest_framework.routers import DefaultRouter

from .views import HabitViewSet, PublicHabitViewSet

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')
router.register(r'public-habits', PublicHabitViewSet, basename='public-habits')

urlpatterns = router.urls

from django.urls import path, include
from home.views import PersonView, PeopleView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'peopel', PeopleView, basename='people')
urlpatterns = router.urls

urlpatterns = [
    path('person', PersonView.as_view()),
    path('people', include(router.urls))
]

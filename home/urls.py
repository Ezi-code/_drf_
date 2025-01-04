from django.urls import path
from .views import PersonView, PeopleView, RegisterView, LoginView, PersonDetailView

app_name = "home"

urlpatterns = [
    path("person", PersonView.as_view()),
    path("person/<int:pk>", PersonDetailView.as_view()),
    path("people", PeopleView.as_view({"get": "list"})),
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
]

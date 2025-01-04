"""Views for the home app."""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person
from .serializer import PersonSerializer, RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator
from drf_spectacular.utils import extend_schema


class PersonView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses={200: PersonSerializer(many=True)})
    def get(self, request):
        try:
            objs = Person.objects.all()
            page = request.GET.get("page", 1)
            pag_size = 3
            paginator = Paginator(objs, pag_size)
            serializer = PersonSerializer(paginator.page(page), many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": str(e),
                },
                status.HTTP_204_NO_CONTENT,
            )

    @extend_schema(request=PersonSerializer, responses={201: PersonSerializer})
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class PersonDetailView(APIView):
    """Person detail view."""

    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(responses={200: PersonSerializer})
    def put(self, request, pk=None):
        person = self.get_object(pk)
        serializer = PersonSerializer(person, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.errors, status.HTTP_201_CREATED)

    @extend_schema(responses={200: PersonSerializer})
    def patch(self, request, pk=None):
        person = self.get_object(pk)
        serializer = PersonSerializer(person, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, pk=None):
        person = self.get_object(pk)
        person.delete()
        return Response(status.HTTP_200_OK)


@api_view(["GET"])
def index(request):
    if request.method == "GET":
        objs = Person.objects.all()
        serializer = PersonSerializer(objs, many=True)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["GET", "POST", "PUT", "PATCH"])
def add_post(request):
    if request.method == "GET":
        objs = Person.objects.filter(color__is_null=True)
        serializer = PersonSerializer(objs, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "PUT":
        data = request.data
        objs = Person.objects.get(id=data["id"])
        serializer = PersonSerializer(objs, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == "PATCH":
        data = request.data
        objs = Person.objects.get(id=data["id"])
        serializer = PersonSerializer(objs, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


@extend_schema(responses={200: PersonSerializer(many=True)})
class PeopleView(viewsets.ModelViewSet):
    """People view."""

    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def list(self, request):
        search = request.GET.get("q")
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__icontains=search)
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)


class RegisterView(APIView):
    """Register view."""

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginView(APIView):
    """Login view."""

    permission_classes = [AllowAny]

    @extend_schema(request=LoginSerializer)
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            user = authenticate(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)

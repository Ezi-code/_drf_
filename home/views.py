from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person
from .serializer import PersonSerializaer, RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class PersonView(APIView):
    def get(self, request):
        objs = Person.objects.all()
        serializer = PersonSerializaer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = PersonSerializaer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self, request):
        data = request.data
        objs = Person.objects.get(id=data['id'])
        serializer = PersonSerializaer(objs, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        objs = Person.objects.get(id=data['id'])
        serializer = PersonSerializaer(objs, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request):
        data = request.data
        objs = Person.objects.get(id=data['id'])
        objs.delete()
        return Response("Deleted")


@api_view(['GET'])
def index(request):
    if request.method == 'GET':
        objs = Person.objects.all()
        serializer = PersonSerializaer(objs, many=True)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'POST', 'PUT', 'PATCH'])
def add_post(request):
    if request.method == 'GET':
        objs = Person.objects.filter(color__is_null=True)
        serializer = PersonSerializaer(objs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PersonSerializaer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'PUT':
        data = request.data
        objs = Person.objects.get(id=data['id'])
        serializer = PersonSerializaer(objs, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PATCH':
        data = request.data
        objs = Person.objects.get(id=data['id'])
        serializer = PersonSerializaer(objs, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class PeopleView(viewsets.ModelViewSet):
    serializer_class = PersonSerializaer
    queryset = Person.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__icontains=search)
        serializer = PersonSerializaer(queryset, many=True)
        return Response(serializer.data)


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "user created",
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():

            user = authenticate(
                username=serializer.data['username'],             password=serializer.data['password'])
            token, _ = Token.objects.get_or_create(user=user)

        if not user:
            return Response({
                "status": False,
                "message": "Invalid Credentials",
            }, status.HTTP_403_FORBIDDEN)

        if user:
            return Response({
                "status": True,
                "message": "Login success",
                "token": str(token)
            }, status.HTTP_202_ACCEPTED)

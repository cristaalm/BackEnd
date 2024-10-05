from .controllers.serializers import MyTokenObtainPairSerializer, RolSeralizer, StatusSerializer, UsersSerializer, RegisterSerializer, DecryptSerializer, decrypt
from myApp.models import Rol, Status, UserData
from django.core.files.storage import default_storage
from django.db import IntegrityError
import os
import uuid

########################################################################################
# Importaciones de Django REST Framework
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny  
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework.reverse import reverse 
from rest_framework_simplejwt.views import TokenObtainPairView
########################################################################################

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
   
class DecryptView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DecryptSerializer(data=request.data)
        if serializer.is_valid():
            encrypted_text = serializer.validated_data['encrypted_text']
            try:
                decrypted_text = decrypt(encrypted_text, "cuatro_veinte")  # Call the decrypt function
                return Response({'decrypted_text': decrypted_text}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # validamos si el request es de tipo multipart/form-data
        if request.content_type !=  'application/json':
            # Manejar la imagen # Extraer la imagen del request
            users_photo = request.data.get('users_photo', None)

            if isinstance(users_photo, str) != True and users_photo and hasattr(users_photo, 'read'):
                # Caso FormData: Subir el archivo a un directorio y guardar la ruta
                filename = f"{uuid.uuid4()}.jpg"  # Generar nombre único
                path = os.path.join('usersImages', filename)
                default_storage.save(path, users_photo)  # Aquí 'users_photo' debe ser un archivo
                request.data['users_photo'] = f'media/usersImages/{filename}'

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = serializer.save()

                # En lugar de generar el token manualmente, usamos el serializer de MyTokenObtainPairSerializer
                token_serializer = MyTokenObtainPairSerializer(data={
                    'username': user.username,  # Usa el campo username del usuario
                    'email': user.email,  # El email enviado en el request
                    'password': request.data.get('password')  # El password enviado en el request
                })

                if token_serializer.is_valid():
                    return Response(token_serializer.validated_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except IntegrityError:
                return Response({"error": "A user with this information already exists."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

########################################################################################

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # Custom action to filter users by id_rol
    @action(detail=False, methods=['get'], url_path='by-id-rol')
    def getByRol(self, request):
        id_rol = request.query_params.get('id_rol', None)
        if id_rol:
            # Filtra y selecciona solo los campos 'id' y 'name'
            users_by_rol = UserData.objects.filter(users_rol=id_rol).values('id', 'name','email')
            return Response(users_by_rol)  # Ya no es necesario usar el serializer, ya que solo devuelves campos seleccionados
        else:
            return Response({'error': 'id_rol no proporcionado'}, status=400)

########################################################################################

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

########################################################################################

class RolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSeralizer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
########################################################################################

# Custom APIVIEW para el API Root

class CustomAPIRootView(APIView):

    # Vista personalizada para el API Root. Añadir manualmente las URLs de las otras apps para que aparezcan en el API Root

    def get(self, request, *args, **kwargs):
        return Response({
            'users': reverse('users-list', request=request, format=kwargs.get('format')),
            'roles': reverse('rol-list', request=request, format=kwargs.get('format')),
            'statuses': reverse('status-list', request=request, format=kwargs.get('format')),
            'areas': reverse('areas-list', request=request, format=kwargs.get('format')),
            'programs': reverse('programs-list', request=request, format=kwargs.get('format')),
            'activities': reverse('activities-list', request=request, format=kwargs.get('format')),
            'days': reverse('days-list', request=request, format=kwargs.get('format')),
            'schedules': reverse('schedules-list', request=request, format=kwargs.get('format')),
            'donations': reverse('donations-list', request=request, format=kwargs.get('format')),
            'bills': reverse('bills-list', request=request, format=kwargs.get('format')),
            'children': reverse('childrens-list', request=request, format=kwargs.get('format')),
        })

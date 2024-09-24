from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from myApp.models import Children
from .serializers import ChildrensSerializer



class ChildrensViewSet(viewsets.ModelViewSet):
    queryset = Children.objects.all()
    serializer_class = ChildrensSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Children successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
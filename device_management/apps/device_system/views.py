from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import EmployeeSerializer,DeviceSerializer,DeviceLogSerializer
from .models import Employee,Device,DeviceLog
from rest_framework import generics


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'status':403,'errors':serializer.errors,'message':'Somthing went wrong'})
        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        return Response({'status':200,'payload':serializer.data})
    

class LoginView(APIView):
    def post(self, request):
        # Retrieve username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log in the user
            login(request, user)

            # Generate or retrieve the user's token
            token, created = Token.objects.get_or_create(user=user)

            # Serialize user data
            serializer = UserSerializer(user)

            # Return user data along with the token
            return Response({
                'status': 200,
                'token': token.key,
                'user_data': serializer.data,
            })
        else:
            # If authentication fails, return an error response
            return Response({'status': 403, 'message': 'Invalid credentials'})

class EmployeeView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        # Only retrieve the employees associated with the current user
        return Employee.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associate the employee with the current user during creation
        serializer.save(user=self.request.user)

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        # Only retrieve the employee associated with the current user
        return Employee.objects.filter(user=self.request.user)



class DeviceLogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve all device logs associated with the current user
        device_logs = DeviceLog.objects.filter(user=request.user)
        serializer = DeviceLogSerializer(device_logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a new device log entry
        serializer = DeviceLogSerializer(data=request.data)
        if serializer.is_valid():
            # Set the user to the current authenticated user
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeviceLogDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        # Retrieve a specific device log by its primary key
        return get_object_or_404(DeviceLog, pk=pk, user=self.request.user)

    def get(self, request, pk):
        # Retrieve details of a specific device log
        device_log = self.get_object(pk)
        serializer = DeviceLogSerializer(device_log)
        return Response(serializer.data)

    def put(self, request, pk):
        # Update details of a specific device log
        device_log = self.get_object(pk)
        serializer = DeviceLogSerializer(device_log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Delete a specific device log
        device_log = self.get_object(pk)
        device_log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeviceView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        # Only retrieve the employees associated with the current user
        return Device.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associate the employee with the current user during creation
        serializer.save(user=self.request.user)

class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        # Only retrieve the employee associated with the current user
        return Device.objects.filter(user=self.request.user)

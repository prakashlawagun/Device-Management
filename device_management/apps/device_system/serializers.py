from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Employee,Device,DeviceLog

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class EmployeeSerializer(serializers.ModelSerializer):
        class Meta:
            model = Employee
            fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
        class Meta:
            model = Device
            fields = '__all__'


class DeviceLogSerializer(serializers.ModelSerializer):
            class Meta:
                model = DeviceLog
                fields = '__all__'

from rest_framework import serializers
from test_task.password_manager.models import PasswordEntry

class PasswordEntrySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    service_name = serializers.CharField()

    class Meta:
        model = PasswordEntry
        fields = ['service_name', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        entry = PasswordEntry(**validated_data)
        entry.set_password(password)
        entry.save()
        return entry

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['password'] = instance.get_password()
        return representation

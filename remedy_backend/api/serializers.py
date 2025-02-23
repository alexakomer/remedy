from rest_framework import serializers
from services.models import Service, ServiceCategory, Provider, ServiceListing, Booking
from django.contrib.auth.models import User

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'business_name', 'description', 'profile_image', 
                 'years_of_experience', 'rating', 'service_area']

class ServiceListingSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)
    
    class Meta:
        model = ServiceListing
        fields = ['id', 'name', 'description', 'provider', 'duration', 
                 'price', 'available_days', 'start_time', 'end_time']

class ServiceSerializer(serializers.ModelSerializer):
    listings = ServiceListingSerializer(many=True, read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'name', 'category', 'description', 'image', 'listings']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class BookingSerializer(serializers.ModelSerializer):
    service_details = ServiceSerializer(source='service', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'service_listing', 'date', 'time', 
            'location', 'special_requests', 'status',
            'service_details', 'user_details'
        ]
        read_only_fields = ['status'] 
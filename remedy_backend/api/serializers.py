from rest_framework import serializers
from services.models import Service, ServiceCategory, Provider, ServiceListing, Booking
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'business_name', 'description', 'profile_image', 
                 'years_of_experience', 'rating', 'service_area']

class ServiceListingSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.business_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta:
        model = ServiceListing
        fields = ['id', 'name', 'description', 'price', 'duration', 
                 'provider', 'provider_name', 'service', 'service_name',
                 'available_days', 'start_time', 'end_time']

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
    service_details = ServiceListingSerializer(source='service_listing', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 
            'user', 
            'user_name',
            'service_listing', 
            'service_details',
            'date', 
            'time', 
            'location', 
            'special_requests', 
            'status', 
            'created_at'
        ]
        read_only_fields = ['user', 'status', 'created_at']

    def validate(self, data):
        """
        Check that the booking date and time are valid
        """
        # Ensure date is not in the past
        if data['date'] < timezone.now().date():
            raise serializers.ValidationError("Cannot book for a past date")
        
        # Check if the time slot is available
        listing = data['service_listing']
        booking_time = data['time']
        
        # Convert day of week to string format used in available_days
        booking_day = str(data['date'].weekday())
        
        # Check if service is available on this day
        if booking_day not in listing.available_days.split(','):
            raise serializers.ValidationError("Service is not available on this day")
        
        # Check if time is within provider's hours
        if booking_time < listing.start_time or booking_time > listing.end_time:
            raise serializers.ValidationError("Selected time is outside of provider's working hours")
        
        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)  # Make email optional
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user 
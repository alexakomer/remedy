from django.shortcuts import render
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer, BookingSerializer, ServiceSerializer, ServiceListingSerializer, ProviderSerializer, UserRegistrationSerializer
from services.models import Booking, Service, ServiceListing, Provider
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            status='pending'
        )

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            error_message = str(e.detail) if isinstance(e.detail, str) else str(e.detail.get(next(iter(e.detail))))
            return Response(
                {'error': error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        # Only allow cancellation of pending or confirmed bookings
        if booking.status in ['pending', 'confirmed']:
            booking.status = 'cancelled'
            booking.save()
            return Response({'status': 'Booking cancelled'})
        return Response(
            {'error': 'Cannot cancel this booking'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        # Get upcoming bookings for the user
        upcoming = self.get_queryset().filter(
            date__gte=datetime.now().date(),
            status__in=['pending', 'confirmed']
        )
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def listings(self, request, pk=None):
        """
        Get all listings for a specific service
        Endpoint: /api/services/{service_id}/listings/
        """
        service = self.get_object()
        listings = ServiceListing.objects.filter(service=service)
        serializer = ServiceListingSerializer(listings, many=True)
        return Response(serializer.data)

class ServiceListingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ServiceListingSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """
        Filter listings by service_id if provided in query params
        Example: /api/listings/?service=1
        """
        queryset = ServiceListing.objects.all()
        service_id = self.request.query_params.get('service', None)
        if service_id is not None:
            queryset = queryset.filter(service_id=service_id)
        return queryset

class ProviderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def listings(self, request, pk=None):
        """
        Get all listings for a specific provider
        Endpoint: /api/providers/{provider_id}/listings/
        """
        provider = self.get_object()
        service_id = request.query_params.get('service', None)
        listings = provider.listings.all()
        
        if service_id:
            listings = listings.filter(service_id=service_id)
            
        serializer = ServiceListingSerializer(listings, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    try:
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User registered successfully",
                "username": serializer.validated_data['username']
            }, status=status.HTTP_201_CREATED)
        
        # Provide more detailed error messages
        errors = {}
        for field, error_list in serializer.errors.items():
            errors[field] = str(error_list[0])
        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            "error": "Registration failed",
            "details": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

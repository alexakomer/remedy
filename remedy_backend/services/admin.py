from django.contrib import admin
from .models import ServiceCategory, Service, ServiceListing, Provider, Booking

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'years_of_experience', 'rating', 'service_area')
    search_fields = ('business_name', 'service_area')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(ServiceListing)
class ServiceListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'provider', 'duration', 'price')
    list_filter = ('service', 'provider')
    search_fields = ('name', 'provider__business_name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_listing', 'date', 'time', 'status')
    list_filter = ('status', 'service_listing', 'date')
    search_fields = ('user__username', 'service_listing__name', 'location')

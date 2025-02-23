from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import Service, ServiceCategory, Provider, ServiceListing
from django.utils.timezone import make_aware
from datetime import time

class Command(BaseCommand):
    help = 'Creates test services, providers, and listings'

    def handle(self, *args, **kwargs):
        # Create default category
        category, _ = ServiceCategory.objects.get_or_create(
            name='Beauty & Wellness',
            slug='beauty-wellness',
            description='Premium beauty and wellness services'
        )

        # Create services
        services_data = [
            {
                'name': 'Mobile IV Therapy',
                'description': 'Rejuvenating IV therapy in the comfort of your home',
            },
            {
                'name': 'Self-Tanning',
                'description': 'Professional spray tanning service',
            },
            {
                'name': 'Lash Extensions',
                'description': 'Full set of premium lash extensions',
            },
            {
                'name': 'Hair Styling',
                'description': 'Professional hair styling services',
            },
            {
                'name': 'Makeup Services',
                'description': 'Professional makeup application',
            },
            {
                'name': 'Nail Services',
                'description': 'Professional manicure and pedicure services',
            },
        ]

        services = {}
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                category=category,
                **service_data
            )
            services[service_data['name']] = service

        # Create providers with more variety
        providers_data = [
            # IV Therapy Providers
            {
                'username': 'wellness_pro',
                'business_name': 'Wellness Pro Services',
                'description': 'Expert in IV therapy and wellness treatments',
                'years_of_experience': 5,
                'service_area': 'Greater Seattle Area',
                'services': ['Mobile IV Therapy'],
                'profile_image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500',
            },
            {
                'username': 'vitality_iv',
                'business_name': 'Vitality IV Lounge',
                'description': 'Mobile IV therapy specialists',
                'years_of_experience': 7,
                'service_area': 'Bellevue Area',
                'services': ['Mobile IV Therapy'],
                'profile_image': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=500',
            },
            {
                'username': 'hydration_health',
                'business_name': 'Hydration Health',
                'description': 'Premium mobile IV services',
                'years_of_experience': 4,
                'service_area': 'Downtown Seattle',
                'services': ['Mobile IV Therapy'],
                'profile_image': 'https://images.unsplash.com/photo-1584362917165-526a968579e8?w=500',
            },
            # Tanning Providers
            {
                'username': 'glow_expert',
                'business_name': 'Glow Beauty Studio',
                'description': 'Specialized in tanning and skin care',
                'years_of_experience': 3,
                'service_area': 'Bellevue',
                'services': ['Self-Tanning'],
                'profile_image': 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=500',
            },
            {
                'username': 'bronze_goddess',
                'business_name': 'Bronze Goddess Mobile',
                'description': 'Expert spray tanning services',
                'years_of_experience': 5,
                'service_area': 'Seattle',
                'services': ['Self-Tanning'],
                'profile_image': 'https://images.unsplash.com/photo-1512290923902-8a9f81dc236c?w=500',
            },
            # Add more providers for each service...
        ]

        for provider_data in providers_data:
            username = provider_data.pop('username')
            services_to_offer = provider_data.pop('services')
            profile_image = provider_data.pop('profile_image')
            
            user, _ = User.objects.get_or_create(
                username=username,
                email=f"{username}@example.com",
            )
            
            provider, _ = Provider.objects.get_or_create(
                user=user,
                defaults={
                    **provider_data,
                    'profile_image': profile_image,
                }
            )

            # Create listings for each service this provider offers
            for service_name in services_to_offer:
                service = services[service_name]
                
                if service_name == 'Mobile IV Therapy':
                    listing_variations = [
                        {
                            'name': 'Basic Hydration IV',
                            'description': 'Essential hydration therapy',
                            'duration': 45,
                            'price': 149.99,
                        },
                        {
                            'name': 'Immune Boost IV',
                            'description': 'Vitamin C and immune support',
                            'duration': 60,
                            'price': 199.99,
                        },
                        {
                            'name': 'Recovery Plus IV',
                            'description': 'Premium recovery and wellness',
                            'duration': 75,
                            'price': 249.99,
                        }
                    ]
                elif service_name == 'Self-Tanning':
                    listing_variations = [
                        {
                            'name': 'Express Tan',
                            'description': 'Quick spray tan session',
                            'duration': 30,
                            'price': 69.99,
                        },
                        {
                            'name': 'Custom Airbrush Tan',
                            'description': 'Personalized shade matching',
                            'duration': 45,
                            'price': 89.99,
                        },
                        {
                            'name': 'Premium Contour Tan',
                            'description': 'Includes highlighting and contouring',
                            'duration': 60,
                            'price': 119.99,
                        }
                    ]
                # Add more service variations...

                for variation in listing_variations:
                    ServiceListing.objects.get_or_create(
                        service=service,
                        provider=provider,
                        name=variation['name'],
                        defaults={
                            'description': variation['description'],
                            'duration': variation['duration'],
                            'price': variation['price'],
                            'available_days': '0,1,2,3,4',  # Monday to Friday
                            'start_time': time(9, 0),  # 9 AM
                            'end_time': time(17, 0),   # 5 PM
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Successfully created test services, providers, and listings')) 
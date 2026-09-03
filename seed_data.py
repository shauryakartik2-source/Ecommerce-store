import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')
django.setup()

from store.models import Category, Product

def seed():
    print("Seeding E-Commerce Data...")
    
    # Categories
    cat_audio, _ = Category.objects.get_or_create(name='Audio & Sound', slug='audio', icon='fa-headphones')
    cat_wearables, _ = Category.objects.get_or_create(name='Smart Wearables', slug='wearables', icon='fa-watch-smart')
    cat_tech, _ = Category.objects.get_or_create(name='Computing & Tech', slug='tech', icon='fa-laptop')
    cat_accessories, _ = Category.objects.get_or_create(name='Accessories', slug='accessories', icon='fa-plug')

    products = [
        {
            'name': 'AeroPulse Wireless Noise-Canceling Headphones',
            'description': 'Studio-grade hybrid Active Noise Cancellation, 45-hour playback, lossless spatial audio, and ultra-soft memory foam earcups.',
            'price': 199.99,
            'original_price': 249.99,
            'category': cat_audio,
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80',
            'rating': 4.9,
            'reviews_count': 128,
            'stock': 35,
            'is_featured': True
        },
        {
            'name': 'Titanium Apex Pro Smartwatch',
            'description': 'Aerospace-grade titanium casing, dual-frequency GPS, ECG monitor, 14-day battery life, and 100m water resistance.',
            'price': 299.99,
            'original_price': 349.99,
            'category': cat_wearables,
            'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80',
            'rating': 4.8,
            'reviews_count': 94,
            'stock': 20,
            'is_featured': True
        },
        {
            'name': 'Mechanical CyberDeck RGB Keyboard',
            'description': 'Custom hot-swappable mechanical switches, anodized aluminum chassis, per-key RGB backlighting, and dual wireless mode.',
            'price': 129.50,
            'original_price': 159.99,
            'category': cat_tech,
            'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80',
            'rating': 4.7,
            'reviews_count': 67,
            'stock': 45,
            'is_featured': False
        },
        {
            'name': 'SonicBass Mini Portable Speaker',
            'description': '360-degree immersive sound with dual passive radiators, IP67 dust/waterproof, and integrated carabiner.',
            'price': 59.99,
            'original_price': 79.99,
            'category': cat_audio,
            'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&auto=format&fit=crop&q=80',
            'rating': 4.6,
            'reviews_count': 42,
            'stock': 60,
            'is_featured': False
        },
        {
            'name': 'Quantum Precision Ergonomic Mouse',
            'description': '26,000 DPI optical sensor, sub-1ms wireless latency, customizable side buttons, and magnetic scroll wheel.',
            'price': 89.99,
            'original_price': 109.99,
            'category': cat_tech,
            'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&auto=format&fit=crop&q=80',
            'rating': 4.8,
            'reviews_count': 110,
            'stock': 15,
            'is_featured': True
        },
        {
            'name': 'HyperCharge 100W GaN Fast Charger',
            'description': 'Multi-port USB-C GaN power adapter capable of charging laptops, phones, and tablets simultaneously at full speed.',
            'price': 49.99,
            'original_price': 65.00,
            'category': cat_accessories,
            'image_url': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&auto=format&fit=crop&q=80',
            'rating': 4.9,
            'reviews_count': 85,
            'stock': 50,
            'is_featured': False
        }
    ]

    for p_data in products:
        Product.objects.get_or_create(name=p_data['name'], defaults=p_data)

    print("Data Seeding Complete!")

if __name__ == '__main__':
    seed()

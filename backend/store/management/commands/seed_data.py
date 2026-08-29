from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = "Seed the database with sample categories and products"

    def handle(self, *args, **options):
        categories = {
            'Electronics': [
                ('Wireless Headphones', 2499, 'Over-ear Bluetooth headphones with noise cancellation.',
                 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500'),
                ('Smart Watch', 3999, 'Fitness tracking smart watch with heart-rate monitor.',
                 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500'),
                ('Bluetooth Speaker', 1799, 'Portable speaker with 12-hour battery life.',
                 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500'),
            ],
            'Fashion': [
                ('Denim Jacket', 1899, 'Classic unisex denim jacket.',
                 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500'),
                ('Running Shoes', 2999, 'Lightweight running shoes with cushioned sole.',
                 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500'),
                ('Leather Backpack', 2199, 'Everyday leather backpack, fits a 15-inch laptop.',
                 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500'),
            ],
            'Home & Kitchen': [
                ('Electric Kettle', 999, '1.5L stainless steel electric kettle.',
                 'https://images.unsplash.com/photo-1585155770447-2f66e2a397b5?w=500'),
                ('Non-Stick Pan Set', 1599, '3-piece non-stick cookware set.',
                 'https://images.unsplash.com/photo-1584990347449-a5d9f800a783?w=500'),
            ],
        }

        for cat_name, products in categories.items():
            category, _ = Category.objects.get_or_create(name=cat_name)
            for name, price, description, image_url in products:
                Product.objects.get_or_create(
                    name=name,
                    defaults={
                        'category': category,
                        'price': price,
                        'description': description,
                        'image_url': image_url,
                        'stock': 25,
                    },
                )

        self.stdout.write(self.style.SUCCESS('Sample categories and products created.'))

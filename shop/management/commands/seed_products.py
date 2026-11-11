from django.core.management.base import BaseCommand
from shop.models import Product

SAMPLES = [('SE-001', 'Wireless Headphones', '1299.00', 25, 'Premium over-ear wireless headphones with immersive audio.', '🎧', '#e6dcfa'), ('SE-002', 'Bluetooth Earbuds', '899.00', 40, 'Compact wireless earbuds with a convenient charging case.', '🎵', '#d9eff9'), ('SE-003', 'Smart Watch', '1599.00', 15, 'Stylish smart watch with fitness tracking and notifications.', '⌚', '#f9e5e6'), ('SE-004', 'Portable Speaker', '1099.00', 30, 'Take your favorite music anywhere with this portable speaker.', '🔊', '#e5f3e5'), ('SE-005', 'Laptop Backpack', '749.00', 22, 'Comfortable backpack with padded laptop compartment.', '🎒', '#fff0d9'), ('SE-006', 'Wireless Mouse', '499.00', 50, 'Ergonomic wireless mouse for work, study, and gaming.', '🖱️', '#eee8fa'), ('SE-007', 'Running Shoes', '1899.00', 28, 'Comfortable lightweight sneakers for daily wear.', '👟', '#fff0e6'), ('SE-008', 'Phone Case', '199.00', 85, 'Protective slim phone case for everyday use.', '📱', '#e4f0ff'), ('SE-009', 'Power Bank 10000mAh', '799.00', 34, 'Portable backup battery with USB charging.', '🔋', '#e8f4e9'), ('SE-010', 'Canvas Tote Bag', '349.00', 60, 'Reusable everyday tote bag with roomy storage.', '👜', '#fff1df'), ('SE-011', 'Mechanical Keyboard', '1499.00', 19, 'Compact mechanical keyboard for gaming and work.', '⌨️', '#f0eaff'), ('SE-012', 'USB-C Charging Cable', '149.00', 100, 'Durable USB-C charging cable for compatible devices.', '🔌', '#e4f7f7'), ('SE-013', 'Digital Wrist Watch', '699.00', 31, 'Classic digital watch with a comfortable strap.', '⌚', '#fff0f3'), ('SE-014', 'Mini Desk Fan', '599.00', 42, 'Compact desk fan for home and office.', '🌀', '#e8f5ff'), ('SE-015', 'Travel Water Bottle', '299.00', 48, 'Reusable leak-resistant water bottle.', '🥤', '#f4f1e7'), ('SE-016', 'Gaming Mouse Pad', '249.00', 55, 'Smooth large mouse pad for precise movement.', '🖱️', '#f0eafa')]

class Command(BaseCommand):
    help = 'Add sixteen ShopEase sample products without duplicating existing products.'
    def handle(self, *args, **options):
        created = 0
        for sku, name, price, stock, description, emoji, color in SAMPLES:
            obj, was_created = Product.objects.get_or_create(sku=sku, defaults={
                'name': name, 'price': price, 'stock': stock,
                'description': description, 'thumbnail': f'products/{sku}.svg',
                'is_active': True,
            })
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f'ShopEase: {created} sample products added.'))

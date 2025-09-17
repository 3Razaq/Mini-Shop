import io
import os
import random
from decimal import Decimal

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.models import Category, Product

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:  # pragma: no cover
    Image = None


PRODUCT_NAMES = [
    "Wireless Headphones",
    "Smart Watch",
    "Bluetooth Speaker",
    "Gaming Mouse",
    "Mechanical Keyboard",
    "USB-C Charger",
    "Laptop Stand",
    "External SSD",
    "Noise Cancelling Earbuds",
    "4K Monitor",
]

CATEGORIES = [
    "Audio",
    "Accessories",
    "Computers",
    "Peripherals",
]


def generate_placeholder_image(text: str, width: int = 800, height: int = 600) -> bytes:
    if Image is None:
        return b""  # If Pillow missing, skip image
    img = Image.new("RGB", (width, height), color=(240, 244, 248))
    draw = ImageDraw.Draw(img)
    title = text[:22]
    try:
        font = ImageFont.truetype("Arial.ttf", 36)
    except Exception:
        font = ImageFont.load_default()
    try:
        left, top, right, bottom = draw.textbbox((0, 0), title, font=font)
        tw, th = right - left, bottom - top
    except Exception:
        # Fallback for very old Pillow
        tw, th = font.getsize(title)
    draw.text(((width - tw) / 2, (height - th) / 2), title, fill=(10, 88, 202), font=font)
    bio = io.BytesIO()
    img.save(bio, format="JPEG", quality=85)
    return bio.getvalue()


class Command(BaseCommand):
    help = "Seed the database with mock categories and products"

    def add_arguments(self, parser):
        parser.add_argument("--products", type=int, default=20, help="Number of products to create")

    def handle(self, *args, **options):
        num_products = options["products"]

        self.stdout.write(self.style.MIGRATE_HEADING("Seeding categories..."))
        category_objs = {}
        for name in CATEGORIES:
            cat, _ = Category.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
            category_objs[name] = cat
        self.stdout.write(self.style.SUCCESS(f"Created/ensured {len(category_objs)} categories"))

        self.stdout.write(self.style.MIGRATE_HEADING("Seeding products..."))
        created = 0
        for i in range(num_products):
            name = random.choice(PRODUCT_NAMES)
            variant = random.randint(100, 999)
            full_name = f"{name} {variant}"
            slug = slugify(full_name)
            if Product.objects.filter(slug=slug).exists():
                continue

            category = random.choice(list(category_objs.values()))
            price = Decimal(random.randrange(1999, 49999)) / 100  # 19.99 - 499.99
            stock = random.randint(0, 50)
            description = (
                f"{full_name} is a great product in our {category.name} line. "
                f"It features excellent build quality and performance."
            )

            product = Product(
                category=category,
                name=full_name,
                slug=slug,
                description=description,
                price=price,
                stock=stock,
            )

            # Attach placeholder image if Pillow available
            image_bytes = generate_placeholder_image(full_name)
            if image_bytes:
                product.image.save(f"{slug}.jpg", ContentFile(image_bytes), save=False)

            product.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} new products"))
        self.stdout.write(self.style.SUCCESS("Seeding complete."))



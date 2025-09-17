import io
import random
import time
from requests.utils import quote
from pathlib import Path
try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    Image = None
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
import requests

from products.models import Product


class Command(BaseCommand):
    help = "Fetch sample images for products from Picsum"

    def add_arguments(self, parser):
        parser.add_argument("--overwrite", action="store_true", help="Overwrite existing images")

    def handle(self, *args, **options):
        overwrite = options["overwrite"]
        products = Product.objects.all()
        updated = 0
        for product in products:
            if product.image and not overwrite:
                continue
            # choose a keyword based on product/category for more relevant images
            name = (product.name or "").lower()
            cat = (getattr(product.category, 'name', '') or '').lower()

            # Curated query terms per product to avoid generic keywords like "watch" => sea
            def build_query() -> str:
                if any(k in name for k in ["headphones", "wireless headphones"]):
                    return "headphones,over-ear,product,studio"
                if "earbuds" in name:
                    return "earbuds,true wireless,product"
                if "speaker" in name:
                    return "bluetooth speaker,portable,product"
                if "keyboard" in name:
                    return "mechanical keyboard,keycaps,product"
                if "mouse" in name:
                    return "gaming mouse,rgb,product"
                if any(k in name for k in ["monitor", "4k monitor"]):
                    return "4k monitor,desk,screen,product"
                if any(k in name for k in ["smart watch", "smartwatch"]):
                    return "smartwatch,wearable,wrist,product"
                if "watch" in name:
                    return "wristwatch,watch,product"
                if any(k in name for k in ["charger", "usb-c", "usb c"]):
                    return "usb c charger,wall adapter,product"
                if "laptop stand" in name:
                    return "laptop stand,aluminum,desk,product"
                if any(k in name for k in ["ssd", "external ssd"]):
                    return "external ssd,portable drive,product"
                # fallback to category-based
                if "audio" in cat:
                    return "audio gadget,product"
                if "peripheral" in cat:
                    return "computer peripherals,product"
                if "computer" in cat:
                    return "computer accessory,product"
                if "accessor" in cat:
                    return "tech accessory,product"
                return "electronics,product"

            query = build_query()
            u_query = quote(query)

            # Try multiple sources in order: Unsplash (query terms), LoremFlickr (tags), Picsum seed
            sources = [
                f"https://source.unsplash.com/800x600/?{u_query}",
                f"https://loremflickr.com/800/600/{u_query}",
                f"https://picsum.photos/seed/{u_query}/800/600",
            ]

            # Prefer local curated images if present: static/sample_images/<tag>/*
            content = None
            project_root = Path(__file__).resolve().parents[4]
            tag = (query.split(',')[0] or 'electronics').replace(' ', '_')
            local_dir = project_root / 'static' / 'sample_images' / tag
            if local_dir.exists() and local_dir.is_dir():
                candidates = sorted([p for p in local_dir.iterdir() if p.suffix.lower() in {'.jpg', '.jpeg', '.png'}])
                if candidates:
                    chosen = random.choice(candidates)
                    try:
                        content = Path(chosen).read_bytes()
                    except Exception:
                        content = None

            for url in sources if content is None else []:
                try:
                    resp = requests.get(url, timeout=20)
                    resp.raise_for_status()
                    content = resp.content
                    break
                except Exception as e:
                    self.stderr.write(f"Source failed for {product.name} ({url}): {e}")
                    time.sleep(0.3)

            if not content:
                # final fallback: generate readable placeholder with text
                if Image is not None:
                    text = product.name[:24] if product.name else 'Product'
                    img = Image.new('RGB', (800, 600), color=(245, 247, 250))
                    draw = ImageDraw.Draw(img)
                    try:
                        font = ImageFont.truetype("Arial.ttf", 40)
                    except Exception:
                        font = ImageFont.load_default()
                    try:
                        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
                        tw, th = right - left, bottom - top
                    except Exception:
                        tw, th = font.getsize(text)
                    draw.text(((800 - tw) / 2, (600 - th) / 2), text, fill=(10, 88, 202), font=font)
                    buf = io.BytesIO()
                    img.save(buf, format='JPEG', quality=85)
                    content = buf.getvalue()
                else:
                    content = b"\xff\xd8\xff\xd9"  # minimal JPEG marker

            filename = f"{product.slug or product.id}.jpg"
            product.image.save(filename, ContentFile(content), save=True)
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Updated images for {updated} products"))



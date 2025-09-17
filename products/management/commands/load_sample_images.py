import io
from pathlib import Path
from random import randint

from django.core.management.base import BaseCommand

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:  # pragma: no cover
    Image = None


TAGS = [
    "headphones",
    "earbuds",
    "speaker",
    "mechanical_keyboard",
    "gaming_mouse",
    "monitor",
    "smartwatch",
    "charger",
    "laptop_stand",
    "ssd",
]


class Command(BaseCommand):
    help = "Generate local curated sample images under static/sample_images/<tag>/*.jpg"

    def add_arguments(self, parser):
        parser.add_argument("--per-tag", type=int, default=3, help="Images per tag")

    def handle(self, *args, **options):
        if Image is None:
            self.stderr.write("Pillow not available; cannot generate images")
            return

        project_root = Path(__file__).resolve().parents[4]
        base_dir = project_root / "static" / "sample_images"
        base_dir.mkdir(parents=True, exist_ok=True)

        created = 0
        for tag in TAGS:
            tag_dir = base_dir / tag
            tag_dir.mkdir(parents=True, exist_ok=True)
            for i in range(options["per_tag"]):
                w, h = 800, 600
                # soft random pastel background
                bg = (randint(200, 245), randint(210, 250), randint(220, 255))
                img = Image.new("RGB", (w, h), color=bg)
                draw = ImageDraw.Draw(img)
                title = tag.replace("_", " ").title()
                subtitle = "Sample Image"
                try:
                    font_title = ImageFont.truetype("Arial.ttf", 48)
                    font_sub = ImageFont.truetype("Arial.ttf", 28)
                except Exception:
                    font_title = ImageFont.load_default()
                    font_sub = ImageFont.load_default()
                try:
                    l1, t1, r1, b1 = draw.textbbox((0, 0), title, font=font_title)
                    tw1, th1 = r1 - l1, b1 - t1
                    l2, t2, r2, b2 = draw.textbbox((0, 0), subtitle, font=font_sub)
                    tw2, th2 = r2 - l2, b2 - t2
                except Exception:
                    tw1, th1 = font_title.getsize(title)
                    tw2, th2 = font_sub.getsize(subtitle)
                draw.text(((w - tw1) / 2, h / 2 - th1 - 6), title, fill=(10, 88, 202), font=font_title)
                draw.text(((w - tw2) / 2, h / 2 + 6), subtitle, fill=(30, 41, 59), font=font_sub)

                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=88)
                (tag_dir / f"{i+1}.jpg").write_bytes(buf.getvalue())
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Generated {created} images under {base_dir}"))



from django.db import models

# Session-based cart; model not strictly required. Placeholder for potential DB cart.
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Cart {self.id}"

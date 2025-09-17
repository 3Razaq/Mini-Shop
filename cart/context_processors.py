from typing import Dict, Any


def cart_counts(request) -> Dict[str, Any]:
    cart = request.session.get('cart', {})
    wishlist = request.session.get('wishlist', set())
    # wishlist stored as list in session, convert to length safely
    if isinstance(wishlist, set):
        wishlist_count = len(wishlist)
    else:
        try:
            wishlist_count = len(list(wishlist))
        except Exception:
            wishlist_count = 0
    count = 0
    for item in cart.values():
        try:
            count += int(item.get('quantity', 0))
        except Exception:
            continue
    return {
        'cart_count': count,
        'wishlist_count': wishlist_count,
    }



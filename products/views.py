from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Product, Category, Review
from .forms import ReviewForm


def product_list(request):
    query = request.GET.get('q')
    category_slug = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products_qs = Product.objects.all()
    categories = Category.objects.all()

    if category_slug:
        products_qs = products_qs.filter(category__slug=category_slug)

    if query:
        products_qs = products_qs.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if min_price:
        try:
            products_qs = products_qs.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            products_qs = products_qs.filter(price__lte=float(max_price))
        except ValueError:
            pass

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products_qs = products_qs.order_by('price')
    elif sort == 'price_desc':
        products_qs = products_qs.order_by('-price')
    elif sort == 'newest':
        products_qs = products_qs.order_by('-created_at')

    paginator = Paginator(products_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
    }

    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    avg_rating = product.reviews.all().aggregate(Avg('rating')).get('rating__avg')
    form = ReviewForm()

    if request.method == 'POST' and request.POST.get('action') == 'review':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rv = form.save(commit=False)
            rv.product = product
            rv.save()
            return redirect('product_detail', slug=product.slug)

    return render(request, 'products/product_detail.html', {
        'product': product,
        'avg_rating': avg_rating,
        'review_form': form,
    })


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

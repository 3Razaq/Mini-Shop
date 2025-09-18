# 🛒 Mini-Shop (Django)

A simple, professional e-commerce demo built with Django 4.2+. Includes product catalog, cart, checkout, reviews, wishlist, admin CRUD, and dynamic image handling. Built for learning, prototyping, or extension.

---

## 🚀 Features

- ✅ Product catalog: categories, brands, price, stock, tags, descriptions
- 🔍 Search, filter (category, price), sort, pagination
- ⭐ Reviews: rating + comments
- 🛒 Cart & wishlist (session-based)
- 👤 Guest & authenticated checkout
- 📦 Order creation with totals
- 🛠 Admin panel with full CRUD
- 🖼 Product images: load local samples or fetch via CLI

---

## 🧰 Tech Stack

- Python 3.9+
- Django 4.2+
- SQLite (default)
- Django Templates + CSS (no JS framework)
- Virtualenv for isolation

---

## 📦 Requirements

- Python 3.9 or newer
- pip (Python package installer)
- virtualenv (recommended)

---

## 🔧 Installation & Setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd Mini-Shop

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Migrate the database
python manage.py migrate

# 6. Create an admin user
python manage.py createsuperuser

# 7. (Optional) Add sample data
python manage.py seed_shop --products 30

# 8. (Optional) Load & fetch sample images
python manage.py load_sample_images --per-tag 4
python manage.py fetch_images --overwrite

# 9. Run the development server
python manage.py runserver

```

Visit:
- Home: http://127.0.0.1:8000/
- Cart: http://127.0.0.1:8000/cart/
- Checkout: http://127.0.0.1:8000/checkout/
- Categories: http://127.0.0.1:8000/categories/
- Wishlist: http://127.0.0.1:8000/wishlist/
- Admin: http://127.0.0.1:8000/admin/
- Login: http://127.0.0.1:8000/accounts/login/
- Signup: http://127.0.0.1:8000/accounts/signup/


## Project Structure (key parts)
```

Mini-Shop/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── shop/              # Project settings and URLs
├── products/          # Product models, views, admin, etc.
├── orders/            # Checkout and order logic
├── cart/              # Cart & wishlist logic
├── accounts/          # Signup/login/views
├── templates/         # All HTML templates
├── static/            # CSS and static assets
└── media/             # Uploaded product images

## Installation
```
Clone the project:

```bash
git clone <your-repo-url>
cd Mini-Shop
code .

```
## Trello
https://trello.com/b/sIjzGYty/call-of-duty

```
```
## ERD

https://www.canva.com/design/DAGzOLtI4IA/h-TYOAqrHrbI6Min4FGeCA/edit?utm_content=DAGzOLtI4IA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

```
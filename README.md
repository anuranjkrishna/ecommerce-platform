🛍️ E-Commerce Platform
A full-stack e-commerce application featuring a product catalog, shopping cart, JWT-based authentication, and a complete checkout flow with online payment support.
![Backend](https://img.shields.io/badge/Backend-Django%20REST%20Framework-092E20?logo=django&logoColor=white)
![Frontend](https://img.shields.io/badge/Frontend-React%20(Vite)-61DAFB?logo=react&logoColor=black)
![Auth](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)
![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Payments](https://img.shields.io/badge/Payments-Razorpay-02042B?logo=razorpay&logoColor=white)
---
📋 Overview
This project is a complete online store, built as a decoupled full-stack application:
Backend — Django REST Framework API handling authentication, product catalog, cart, and order management.
Frontend — A React (Vite) single-page application consuming the API.
Layer	Technology
Backend	Django, Django REST Framework, SimpleJWT, django-cors-headers
Database	SQLite (default, zero setup) — PostgreSQL-ready
Frontend	React (Vite), React Router, Axios
Payments	Razorpay (test mode) + Cash on Delivery
✨ Features
🔐 JWT authentication with automatic token refresh
🛒 Full shopping cart (add, update quantity, remove items)
📦 Product catalog with categories and search
💳 Checkout with Cash on Delivery or Razorpay online payment
🧾 Order history with item-level detail and payment status
🖼️ Image upload for products directly from the Django admin
🗄️ Swappable database — SQLite out of the box, PostgreSQL-ready for production
🖼️ Screenshots
Home / Product Grid	Product Detail
![Home page screenshot](./screenshots/home.png)	![Product detail screenshot](./screenshots/product-detail.png)

Cart	Checkout
![Cart screenshot](./screenshots/cart.png)	![Checkout screenshot](./screenshots/checkout.png)

Order History	Django Admin
![Orders screenshot](./screenshots/orders.png)	![Admin panel screenshot](./screenshots/admin.png)
> Replace the files above with your own screenshots — create a `screenshots/` folder at the project root and drop in PNGs with these exact names (`home.png`, `product-detail.png`, `cart.png`, `checkout.png`, `orders.png`, `admin.png`), or update the paths/filenames to match whatever you use.
📁 Project Structure
```
ecommerce-project/
├── backend/      # Django REST Framework API
└── frontend/     # React (Vite) single-page application
```
<details>
<summary><strong>Backend structure (<code>backend/store/</code>)</strong></summary>
File	Purpose
`models.py`	`Category`, `Product`, `Cart`, `CartItem`, `Order`, `OrderItem`
`serializers.py`	DRF serializers for all models, plus register/checkout logic
`views.py`	Auth (register/login/refresh), product browsing, cart operations, checkout, order history
`urls.py`	All `/api/...` routes
`management/commands/seed_data.py`	Sample data generator (categories & products)
</details>
<details>
<summary><strong>Frontend structure (<code>frontend/src/</code>)</strong></summary>
File / Folder	Purpose
`api/axios.js`	Pre-configured API client with automatic JWT refresh
`context/AuthContext.jsx`	Global authentication state
`context/CartContext.jsx`	Global cart state
`pages/`	`Home`, `ProductDetail`, `Cart`, `Checkout`, `Login`, `Register`, `Orders`
`components/`	`Navbar`, `ProductCard`
`App.jsx`	Route definitions, including protected routes for Cart/Checkout/Orders
</details>
---
🚀 Getting Started
Prerequisites
Python 3.10+
Node.js 18+
npm
1. Backend Setup (Django API)
Open a terminal in the `backend/` folder:
```bash
cd backend

# 1. Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations (creates the database tables)
python manage.py migrate

# 4. Load sample products & categories
python manage.py seed_data

# 5. (Optional) create an admin login to view data at /admin
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```
Resource	URL
API root	http://127.0.0.1:8000/api/products/
Admin panel	http://127.0.0.1:8000/admin/
2. Frontend Setup (React)
Open a second terminal in the `frontend/` folder — keep the backend running in the first one:
```bash
cd frontend
npm install
npm run dev
```
The storefront is now running at http://localhost:5173/.
---
💳 Enabling Online Payments (Razorpay — optional)
Cash on Delivery works out of the box with zero setup. To also enable the "Pay Online" option:
Create a free account at dashboard.razorpay.com/signup.
Go to Settings → API Keys → Generate Test Key (test mode — no real money, no KYC required).
Copy the Key ID and Key Secret.
Set them as environment variables before starting the backend:
```powershell
# Windows PowerShell
$env:RAZORPAY_KEY_ID="rzp_test_xxxxxxxxxxxx"
$env:RAZORPAY_KEY_SECRET="xxxxxxxxxxxxxxxxxxxx"
python manage.py runserver
```
```bash
# Mac/Linux
export RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxx
export RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxx
python manage.py runserver
```
On the checkout page, selecting "Pay Online" opens the Razorpay popup. Use Razorpay's published test card to simulate a successful payment — no real charge occurs in test mode:
> **Card:** `4111 1111 1111 1111` &nbsp;·&nbsp; **Expiry:** any future date &nbsp;·&nbsp; **CVV:** any 3 digits
> If these environment variables are not set, Cash on Delivery continues to work normally — "Pay Online" simply shows a clear, handled error instead of crashing.
🗄️ Switching to PostgreSQL (optional)
The project uses SQLite by default for zero-setup local development. To switch to PostgreSQL:
Open `backend/ecommerce_backend/settings.py`.
Comment out the SQLite `DATABASES` block.
Uncomment the PostgreSQL block just below it.
Set the following environment variables (or edit the defaults directly):
`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
---
✅ Verifying the Setup
Walk through this checklist to confirm everything is wired up correctly:
Visit http://localhost:5173/ — the product grid should appear (Electronics, Fashion, Home & Kitchen).
Click Register → create an account → you're logged in automatically.
Click any product → Add to Cart.
Click Cart (top right, shows an item-count badge) → adjust quantity or remove items.
Click Proceed to Checkout → enter a shipping address → choose Cash on Delivery or Pay Online (test card above) → place the order.
You'll land on My Orders, showing the order with items, total, and payment status (Paid / Cash on Delivery).
Refresh the page — you remain logged in (JWT token persisted in the browser).
(Optional) Visit http://127.0.0.1:8000/admin/ and sign in with your superuser to view Users, Products, Carts, and Orders directly.
> **Troubleshooting:** a network error on any page almost always means the backend isn't running — confirm `python manage.py runserver` is still active in its terminal.
🖼️ Adding Products with a Real Image
In the Django admin (`/admin/`), go to Products → Add Product. The Image field includes a "Choose File" button — select a photo directly from your computer; no need to host it externally. Alternatively, leave Image empty and paste a link into Image URL — the site automatically uses whichever field is filled in.
---
📡 API Reference
All endpoints are prefixed with `/api/`.
Method	Endpoint	Auth	Description
`POST`	`/auth/register/`	–	Create a new account
`POST`	`/auth/login/`	–	Obtain JWT access + refresh tokens
`POST`	`/auth/refresh/`	–	Refresh an expired access token
`GET`	`/products/`	–	List products (supports `?search=` & `?category=`)
`GET`	`/products/<slug>/`	–	Retrieve product detail
`GET`	`/categories/`	–	List categories
`GET`	`/cart/`	✅	View the current user's cart
`POST`	`/cart/add/`	✅	Add an item — `{ product_id, quantity }`
`PUT`	`/cart/update/<item_id>/`	✅	Update item quantity — `{ quantity }`
`DELETE`	`/cart/remove/<item_id>/`	✅	Remove an item from the cart
`POST`	`/orders/checkout/`	✅	Cash on Delivery — create order from cart — `{ shipping_address }`
`POST`	`/orders/razorpay/create/`	✅	Create a Razorpay order for the cart total — `{ shipping_address }`
`POST`	`/orders/razorpay/verify/`	✅	Verify payment & create order — `{ shipping_address, razorpay_order_id, razorpay_payment_id, razorpay_signature }`
`GET`	`/orders/`	✅	Retrieve the current user's order history
`GET`	`/orders/<id>/`	✅	Retrieve a single order's detail
---
🧰 Tech Stack Summary
Backend: Django · Django REST Framework · SimpleJWT · django-cors-headers
Frontend: React · Vite · React Router · Axios
Database: SQLite (dev) · PostgreSQL (production-ready)
Payments: Razorpay (test mode) + Cash on Delivery
---
<p align="center">Built with Django REST Framework &amp; React</p>

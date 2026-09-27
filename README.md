E-commerce Platform — Django REST Framework + React.js
Full-stack e-commerce app: product catalog, cart, JWT auth, and checkout/order history.

Backend: Django, Django REST Framework, SimpleJWT, django-cors-headers (SQLite by default, PostgreSQL-ready)
Frontend: React (Vite), React Router, Axios
ecommerce-project/
  backend/     -> Django project (API)
  frontend/    -> React app (UI)
1. Backend setup (Django API)
Open a terminal in VS Code, inside the backend folder.

cd backend

# 1. Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations (creates the database tables)
python manage.py migrate

# 4. Add sample products & categories
python manage.py seed_data

# 5. (Optional) create an admin login to view data at /admin
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
Backend now runs at: http://127.0.0.1:8000/ Admin panel: http://127.0.0.1:8000/admin/ API root: http://127.0.0.1:8000/api/products/

Enabling online payments (Razorpay, optional but recommended)
Cash on Delivery works with zero setup. To enable the "Pay Online" option:

Create a free account at https://dashboard.razorpay.com/signup
Go to Settings → API Keys → Generate Test Key (test mode, no real money, no KYC needed)
Copy the Key Id and Key Secret
Before running the backend, set them as environment variables in the same terminal:
# Windows PowerShell
$env:RAZORPAY_KEY_ID="rzp_test_xxxxxxxxxxxx"
$env:RAZORPAY_KEY_SECRET="xxxxxxxxxxxxxxxxxxxx"
python manage.py runserver
# Mac/Linux
export RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxx
export RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxx
python manage.py runserver
On the checkout page, choose "Pay Online" — a Razorpay popup opens. Use Razorpay's published test card 4111 1111 1111 1111, any future expiry, any CVV, to simulate a successful payment. No real charge happens in test mode.
If these env vars aren't set, Cash on Delivery still works fine — the "Pay Online" option will just show a clear error instead of crashing.

Switching to PostgreSQL (optional)
By default the project uses SQLite (zero setup, works immediately). To use PostgreSQL instead, open backend/ecommerce_backend/settings.py, comment out the SQLite DATABASES block, and un-comment the PostgreSQL block just below it. Then set these environment variables (or edit the defaults directly): DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT.

2. Frontend setup (React)
Open a second terminal in VS Code, inside the frontend folder (keep the backend running in the first one).

cd frontend
npm install
npm run dev
Frontend now runs at: http://localhost:5173/

Open that link in your browser — that's the actual store.

3. How to check everything works
Visit http://localhost:5173/ — you should see the product grid (Electronics, Fashion, Home & Kitchen sample products).
Click Register → create an account → you'll be logged in automatically.
Click any product → Add to Cart.
Click Cart (top right, shows a badge with item count) → adjust quantity or remove items.
Click Proceed to Checkout → enter a shipping address → choose Cash on Delivery or Pay Online (Razorpay — needs test keys set, see setup section above) → place the order. For online payment, use test card 4111 1111 1111 1111, any future expiry date, any CVV.
You'll land on My Orders, showing the order you just placed with items, total, and payment status (Paid / Cash on Delivery).
Refresh the page — you're still logged in (JWT token is saved in the browser).
Optional: go to http://127.0.0.1:8000/admin/, log in with the superuser you created, and see the Users, Products, Carts and Orders directly in Django admin.
If a page shows a network error, the most common cause is the backend server not running — make sure python manage.py runserver is still active in its terminal.

Adding your own products with a real image
Go to http://127.0.0.1:8000/admin/, log in with your superuser, click Products → Add Product. There's now a proper Image field with a "Choose File" button — pick a photo from your computer and it uploads directly (no need to paste a URL). If you'd rather link an external image instead, leave Image empty and paste a link into Image url — the site will use whichever one is filled in.

Project structure reference
Backend (backend/store/)

models.py — Category, Product, Cart, CartItem, Order, OrderItem
serializers.py — DRF serializers for all models + register/checkout
views.py — auth (register/login/refresh), product browsing, cart operations, checkout, order history
urls.py — all /api/... routes
management/commands/seed_data.py — sample data generator
Frontend (frontend/src/)

api/axios.js — pre-configured API client with automatic JWT refresh
context/AuthContext.jsx, context/CartContext.jsx — global login & cart state
pages/ — Home, ProductDetail, Cart, Checkout, Login, Register, Orders
components/ — Navbar, ProductCard
App.jsx — routes (including protected routes for Cart/Checkout/Orders)
API endpoints (for reference / Postman testing)
Method	Endpoint	Auth required	Purpose
POST	/api/auth/register/	No	Create account
POST	/api/auth/login/	No	Get JWT access + refresh tokens
POST	/api/auth/refresh/	No	Refresh access token
GET	/api/products/	No	List products (?search= &category=)
GET	/api/products/<slug>/	No	Product detail
GET	/api/categories/	No	List categories
GET	/api/cart/	Yes	View your cart
POST	/api/cart/add/	Yes	Add item {product_id, quantity}
PUT	/api/cart/update/<item_id>/	Yes	Update quantity {quantity}
DELETE	/api/cart/remove/<item_id>/	Yes	Remove item
POST	/api/orders/checkout/	Yes	Cash on Delivery: create order from cart {shipping_address}
POST	/api/orders/razorpay/create/	Yes	Create a Razorpay order for the cart total {shipping_address}
POST	/api/orders/razorpay/verify/	Yes	Verify payment & create order {shipping_address, razorpay_order_id, razorpay_payment_id, razorpay_signature}
GET	/api/orders/	Yes	Your order history
GET	/api/orders/<id>/	Yes	Single order detail

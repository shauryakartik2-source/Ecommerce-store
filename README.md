# CodeAlpha - Task 1: Simple E-Commerce Store 🛒

A full-stack, responsive, high-performance E-Commerce application built for the **CodeAlpha Full Stack Development Internship Program**.

## 🌟 Key Features
- **Modern Glassmorphic Dark UI**: Custom CSS design system with micro-interactions, responsive grid, toast notifications, and dark glass visuals.
- **RESTful API Backend**: Powered by Python 3 & Django Framework with SQLite persistence.
- **Product Catalog & Filtering**: Real-time category filtering (Audio, Wearables, Tech, Accessories) and live search query support.
- **Interactive Shopping Cart**: Slide-out cart drawer with quantity selectors, dynamic subtotal calculations, and cart clear feature.
- **Checkout & Order Processing**: Complete multi-field shipping form, order summary, order status tracking (Pending, Processing, Shipped, Delivered).
- **User Authentication**: Built-in User Registration, Login, Logout, and persistent session state.
- **Order History Dashboard**: Track past orders and their status in real-time.

## 📁 Repository Structure
```
CodeAlpha_ECommerceStore/
├── manage.py
├── seed_data.py
├── ecommerce_backend/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── store/
    ├── models.py       # Category, Product, Cart, CartItem, Order, OrderItem
    ├── views.py        # Django REST Endpoints & Views
    ├── urls.py
    ├── templates/
    │   └── index.html  # Single-Page App HTML Interface
    └── static/
        ├── styles.css  # Full Glassmorphic CSS Design System
        └── app.js      # REST API Integration & UI Logic
```

## 🚀 How to Run Locally

1. **Navigate to the Project Folder**:
   ```bash
   cd CodeAlpha_ECommerceStore
   ```

2. **Run Migrations & Seed Sample Products**:
   ```bash
   python manage.py migrate
   python seed_data.py
   ```

3. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

4. **Open in Browser**:
   Navigate to `http://127.0.0.1:8000/` in your browser.

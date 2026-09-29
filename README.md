# CodeAlpha - Task 1: Simple E-Commerce Store 🛒

A modern, responsive, high-performance E-Commerce web application built for the **CodeAlpha Web Development Internship Program**.

The project is built with **Pure HTML5, CSS3, and Vanilla JavaScript** with complete client-side state persistence (`localStorage`), requiring **zero dependencies or backend servers** to run.

---

## 🌟 Key Features
- **Modern Glassmorphic Dark UI**: Custom CSS design system with micro-interactions, responsive grid, toast notifications, slide-out drawer, and dark glass visuals.
- **Pure Client-Side Architecture**: Runs 100% in the browser. Zero setup or server installation needed.
- **Product Catalog & Filtering**: Real-time category filtering (Audio, Wearables, Tech, Accessories) and live search query support.
- **Interactive Shopping Cart**: Slide-out cart drawer with quantity selectors, dynamic subtotal calculations, and cart clear feature.
- **Checkout & Order Processing**: Complete multi-field shipping form, order summary, order status tracking (Pending, Processing, Shipped, Delivered).
- **User Authentication**: Client-side User Registration, Login, Logout, and persistent session state via `localStorage`.
- **Order History Dashboard**: Track past orders and their status in real-time.
- **GitHub Pages Ready**: Can be deployed and hosted on GitHub Pages with 1 click.

---

## 📁 Repository Structure
```
CodeAlpha_ECommerceStore/
├── index.html        # Main Single-Page HTML Interface
├── styles.css        # Full Glassmorphic CSS Design System
├── app.js            # Standalone Vanilla JS Engine & LocalStorage DB
├── requirements.txt  # Python requirements (for optional Django backend)
├── manage.py         # Django management script
├── seed_data.py      # Django initial seed data script
├── ecommerce_backend/# Django backend configuration
└── store/            # Django app templates, models & views
```

---

## 🚀 How to Run

### Method 1: Direct in Browser (Recommended & Fastest)
Simply double-click **`index.html`** or right click -> **Open with Chrome/Edge/Firefox** (or VS Code Live Server).
*No Python or server setup required!*

### Method 2: Host on GitHub Pages
1. Go to your GitHub repository: `https://github.com/shauryakartik2-source/Ecommerce-store`
2. Go to **Settings** > **Pages**.
3. Under **Branch**, select `main` and root `/ (root)`.
4. Click **Save**. Your site will be live on the web in seconds!

### Method 3: Optional Django Backend
If you want to run the Django full-stack version:
```bash
python -m pip install -r requirements.txt
python manage.py migrate
python seed_data.py
python manage.py runserver
```
Then visit `http://127.0.0.1:8000/`.

---

## 🛠️ Technologies Used
- **HTML5**: Semantic layout & accessible modals
- **CSS3**: Glassmorphism, CSS Variables, Flexbox/Grid, Keyframe Animations
- **Vanilla JavaScript (ES6+)**: DOM manipulation, asynchronous actions, state management
- **LocalStorage API**: Client-side database for Products, Cart, Orders, and Auth
- **FontAwesome 6 & Google Fonts (Outfit)**

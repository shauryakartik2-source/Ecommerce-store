// ========================================================
// NEXUS STORE - Standalone Pure JavaScript Client Engine
// Fully functional with LocalStorage persistence (No backend needed)
// ========================================================

// Currency Formatter - Indian Rupees (₹)
function formatINR(amount) {
    return '₹' + Number(amount).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// Default Data Seed (Indian Rupee Prices)
const DEFAULT_CATEGORIES = [
    { id: 1, name: 'Audio & Sound', slug: 'audio', icon: 'fa-headphones' },
    { id: 2, name: 'Smart Wearables', slug: 'wearables', icon: 'fa-clock' },
    { id: 3, name: 'Computing & Tech', slug: 'tech', icon: 'fa-laptop' },
    { id: 4, name: 'Accessories', slug: 'accessories', icon: 'fa-plug' }
];

const DEFAULT_PRODUCTS = [
    {
        id: 1,
        name: 'AeroPulse Wireless Noise-Canceling Headphones',
        description: 'Studio-grade hybrid Active Noise Cancellation, 45-hour playback, lossless spatial audio, and ultra-soft memory foam earcups.',
        price: 1999.00,
        original_price: 2499.00,
        category_name: 'Audio & Sound',
        category_slug: 'audio',
        image_url: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80',
        rating: 4.9,
        reviews_count: 128,
        stock: 35,
        is_featured: true
    },
    {
        id: 2,
        name: 'Titanium Apex Pro Smartwatch',
        description: 'Aerospace-grade titanium casing, dual-frequency GPS, ECG monitor, 14-day battery life, and 100m water resistance.',
        price: 2999.00,
        original_price: 3499.00,
        category_name: 'Smart Wearables',
        category_slug: 'wearables',
        image_url: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80',
        rating: 4.8,
        reviews_count: 94,
        stock: 20,
        is_featured: true
    },
    {
        id: 3,
        name: 'Mechanical CyberDeck RGB Keyboard',
        description: 'Custom hot-swappable mechanical switches, anodized aluminum chassis, per-key RGB backlighting, and dual wireless mode.',
        price: 1299.00,
        original_price: 1599.00,
        category_name: 'Computing & Tech',
        category_slug: 'tech',
        image_url: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80',
        rating: 4.7,
        reviews_count: 67,
        stock: 45,
        is_featured: false
    },
    {
        id: 4,
        name: 'SonicBass Mini Portable Speaker',
        description: '360-degree immersive sound with dual passive radiators, IP67 dust/waterproof, and integrated carabiner.',
        price: 599.00,
        original_price: 799.00,
        category_name: 'Audio & Sound',
        category_slug: 'audio',
        image_url: 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&auto=format&fit=crop&q=80',
        rating: 4.6,
        reviews_count: 42,
        stock: 60,
        is_featured: false
    },
    {
        id: 5,
        name: 'Quantum Precision Ergonomic Mouse',
        description: '26,000 DPI optical sensor, sub-1ms wireless latency, customizable side buttons, and magnetic scroll wheel.',
        price: 899.00,
        original_price: 1099.00,
        category_name: 'Computing & Tech',
        category_slug: 'tech',
        image_url: 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&auto=format&fit=crop&q=80',
        rating: 4.8,
        reviews_count: 110,
        stock: 15,
        is_featured: true
    },
    {
        id: 6,
        name: 'HyperCharge 100W GaN Fast Charger',
        description: 'Multi-port USB-C GaN power adapter capable of charging laptops, phones, and tablets simultaneously at full speed.',
        price: 499.00,
        original_price: 650.00,
        category_name: 'Accessories',
        category_slug: 'accessories',
        image_url: 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&auto=format&fit=crop&q=80',
        rating: 4.9,
        reviews_count: 85,
        stock: 50,
        is_featured: false
    }
];

// App State
let currentCategory = 'all';
let searchQuery = '';
let cartItems = [];
let currentUser = null;

// Initialize Database in LocalStorage
function initStorage() {
    const STORAGE_VERSION = 'nexus_v2_inr';
    const currentVersion = localStorage.getItem('nexus_version');

    if (currentVersion !== STORAGE_VERSION) {
        localStorage.setItem('nexus_products', JSON.stringify(DEFAULT_PRODUCTS));
        localStorage.setItem('nexus_categories', JSON.stringify(DEFAULT_CATEGORIES));
        localStorage.removeItem('nexus_cart');
        localStorage.setItem('nexus_version', STORAGE_VERSION);
    } else {
        if (!localStorage.getItem('nexus_products')) {
            localStorage.setItem('nexus_products', JSON.stringify(DEFAULT_PRODUCTS));
        }
        if (!localStorage.getItem('nexus_categories')) {
            localStorage.setItem('nexus_categories', JSON.stringify(DEFAULT_CATEGORIES));
        }
    }

    if (!localStorage.getItem('nexus_users')) {
        localStorage.setItem('nexus_users', JSON.stringify([]));
    }
    if (!localStorage.getItem('nexus_orders')) {
        localStorage.setItem('nexus_orders', JSON.stringify([]));
    }
    if (!localStorage.getItem('nexus_cart')) {
        localStorage.setItem('nexus_cart', JSON.stringify([]));
    }

    const savedUser = localStorage.getItem('nexus_current_user');
    currentUser = savedUser ? JSON.parse(savedUser) : null;
    cartItems = JSON.parse(localStorage.getItem('nexus_cart') || '[]');
}

// Lifecycle Init
document.addEventListener('DOMContentLoaded', () => {
    initStorage();
    checkAuthStatus();
    loadCategories();
    loadProducts();
    loadCart();
});

// Toast Notifications
function showToast(message, icon = 'fa-circle-check') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Check Authentication Status
function checkAuthStatus() {
    const userBtnText = document.getElementById('userBtnText');
    const ordersBtn = document.getElementById('ordersBtn');

    if (currentUser) {
        userBtnText.innerText = currentUser.username;
        ordersBtn.style.display = 'inline-flex';
    } else {
        userBtnText.innerText = 'Sign In';
        ordersBtn.style.display = 'none';
    }
}

// Load Categories
function loadCategories() {
    const categories = JSON.parse(localStorage.getItem('nexus_categories') || '[]');
    const container = document.getElementById('categoriesBar');
    if (!container) return;

    let html = `
        <button class="category-chip ${currentCategory === 'all' ? 'active' : ''}" onclick="filterCategory('all')">
            <i class="fa-solid fa-layer-group"></i> All
        </button>
    `;

    categories.forEach(cat => {
        html += `
            <button class="category-chip ${currentCategory === cat.slug ? 'active' : ''}" onclick="filterCategory('${cat.slug}')">
                <i class="fa-solid ${cat.icon}"></i> ${cat.name}
            </button>
        `;
    });
    container.innerHTML = html;
}

// Load Products
function loadProducts() {
    const grid = document.getElementById('productGrid');
    if (!grid) return;

    let products = JSON.parse(localStorage.getItem('nexus_products') || '[]');

    // Filter by Category
    if (currentCategory !== 'all') {
        products = products.filter(p => p.category_slug === currentCategory);
    }

    // Filter by Search Query
    if (searchQuery.trim() !== '') {
        const query = searchQuery.toLowerCase();
        products = products.filter(p => 
            p.name.toLowerCase().includes(query) || 
            p.description.toLowerCase().includes(query)
        );
    }

    if (products.length === 0) {
        grid.innerHTML = `
            <div class="empty-cart" style="grid-column: 1/-1; padding: 4rem;">
                <i class="fa-solid fa-box-open"></i>
                <h3>No products found</h3>
                <p>Try searching for something else or clearing filters.</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = products.map(p => {
        const discount = p.original_price ? Math.round(((p.original_price - p.price) / p.original_price) * 100) : 0;
        return `
            <div class="product-card">
                <div class="product-image-wrap">
                    <img src="${p.image_url}" alt="${p.name}">
                    <span class="product-tag">${p.category_name}</span>
                    ${discount > 0 ? `<span class="discount-tag">-${discount}%</span>` : ''}
                </div>
                <div class="product-details">
                    <div class="product-rating">
                        <i class="fa-solid fa-star"></i>
                        <strong>${p.rating}</strong>
                        <span>(${p.reviews_count} reviews)</span>
                    </div>
                    <h3 class="product-title">${p.name}</h3>
                    <div class="product-price-row">
                        <span class="current-price">${formatINR(p.price)}</span>
                        ${p.original_price ? `<span class="old-price">${formatINR(p.original_price)}</span>` : ''}
                    </div>
                    <div class="product-actions">
                        <button class="add-cart-btn" onclick="addToCart(${p.id})">
                            <i class="fa-solid fa-cart-plus"></i> Add to Cart
                        </button>
                        <button class="quick-view-btn" onclick="openProductModal(${p.id})" title="Quick View">
                            <i class="fa-regular fa-eye"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Category Filter & Search
function filterCategory(slug) {
    currentCategory = slug;
    loadCategories();
    loadProducts();
}

function handleSearch(e) {
    searchQuery = e.target.value;
    const clearBtn = document.getElementById('clearSearchBtn');
    if (clearBtn) {
        clearBtn.style.display = searchQuery ? 'inline-block' : 'none';
    }
    loadProducts();
}

function clearSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) searchInput.value = '';
    searchQuery = '';
    const clearBtn = document.getElementById('clearSearchBtn');
    if (clearBtn) clearBtn.style.display = 'none';
    loadProducts();
}

function scrollToShop() {
    const shop = document.getElementById('shop');
    if (shop) shop.scrollIntoView({ behavior: 'smooth' });
}

// ==========================================
// CART MANAGEMENT (LocalStorage)
// ==========================================
function saveCart() {
    localStorage.setItem('nexus_cart', JSON.stringify(cartItems));
}

function loadCart() {
    cartItems = JSON.parse(localStorage.getItem('nexus_cart') || '[]');

    const countBadge = document.getElementById('cartBadge');
    const itemsContainer = document.getElementById('cartItemsContainer');
    const checkoutBtn = document.getElementById('checkoutTriggerBtn');

    const totalQty = cartItems.reduce((acc, i) => acc + i.quantity, 0);
    if (countBadge) countBadge.innerText = totalQty;

    if (!itemsContainer) return;

    if (cartItems.length === 0) {
        itemsContainer.innerHTML = `
            <div class="empty-cart">
                <i class="fa-solid fa-basket-shopping"></i>
                <h3>Your cart is empty</h3>
                <p>Add some sleek tech products to get started!</p>
            </div>
        `;
        document.getElementById('cartSubtotal').innerText = '₹0.00';
        document.getElementById('cartTotal').innerText = '₹0.00';
        if (checkoutBtn) checkoutBtn.disabled = true;
        return;
    }

    if (checkoutBtn) checkoutBtn.disabled = false;

    const total = cartItems.reduce((acc, item) => acc + (item.price * item.quantity), 0);

    itemsContainer.innerHTML = cartItems.map(item => `
        <div class="cart-item">
            <img src="${item.image_url}" alt="${item.name}">
            <div class="cart-item-info">
                <h4>${item.name}</h4>
                <span class="cart-item-price">${formatINR(item.price)}</span>
            </div>
            <div class="qty-controls">
                <button class="qty-btn" onclick="updateCartQty(${item.id}, ${item.quantity - 1})">-</button>
                <span class="qty-val">${item.quantity}</span>
                <button class="qty-btn" onclick="updateCartQty(${item.id}, ${item.quantity + 1})">+</button>
            </div>
        </div>
    `).join('');

    document.getElementById('cartSubtotal').innerText = formatINR(total);
    document.getElementById('cartTotal').innerText = formatINR(total);
}

function addToCart(productId) {
    const products = JSON.parse(localStorage.getItem('nexus_products') || '[]');
    const product = products.find(p => p.id === productId);
    if (!product) return;

    const existingIndex = cartItems.findIndex(i => i.id === productId);
    if (existingIndex > -1) {
        cartItems[existingIndex].quantity += 1;
    } else {
        cartItems.push({
            id: product.id,
            name: product.name,
            price: product.price,
            image_url: product.image_url,
            quantity: 1
        });
    }

    saveCart();
    loadCart();
    showToast('Item added to cart!', 'fa-bag-shopping');
}

function updateCartQty(productId, quantity) {
    if (quantity <= 0) {
        cartItems = cartItems.filter(i => i.id !== productId);
    } else {
        const item = cartItems.find(i => i.id === productId);
        if (item) item.quantity = quantity;
    }

    saveCart();
    loadCart();
}

function toggleCartDrawer() {
    const drawer = document.getElementById('cartDrawer');
    const overlay = document.getElementById('cartOverlay');
    if (drawer && overlay) {
        drawer.classList.toggle('active');
        overlay.classList.toggle('active');
    }
}

// ==========================================
// MODAL CONTROLLERS
// ==========================================
function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.add('active');
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.remove('active');
}

// Product Quick View Modal
function openProductModal(productId) {
    openModal('productModal');
    const modalBody = document.getElementById('productModalBody');
    if (!modalBody) return;

    const products = JSON.parse(localStorage.getItem('nexus_products') || '[]');
    const p = products.find(item => item.id === productId);
    if (!p) return;

    modalBody.innerHTML = `
        <div class="product-modal-grid">
            <div class="product-modal-image-wrap">
                <img src="${p.image_url}" alt="${p.name}" class="product-modal-image">
            </div>
            <div class="product-modal-details">
                <span class="product-tag product-modal-tag">${p.category_name}</span>
                <h2 class="product-modal-title">${p.name}</h2>
                <div class="product-rating product-modal-rating">
                    <i class="fa-solid fa-star"></i> <strong>${p.rating}</strong> <span>(${p.reviews_count} reviews)</span>
                </div>
                <p class="product-modal-desc">${p.description}</p>
                <div class="product-modal-price">
                    ${formatINR(p.price)}
                </div>
                <button class="btn btn-primary btn-block" onclick="addToCart(${p.id}); closeModal('productModal');">
                    <i class="fa-solid fa-cart-plus"></i> Add to Cart Now
                </button>
            </div>
        </div>
    `;
}

// ==========================================
// CHECKOUT & ORDERS
// ==========================================
function openCheckoutModal() {
    toggleCartDrawer();
    openModal('checkoutModal');

    const total = document.getElementById('cartTotal').innerText;
    document.getElementById('chkSummaryTotal').innerText = total;

    if (currentUser) {
        document.getElementById('chkEmail').value = currentUser.email || '';
        document.getElementById('chkFullName').value = currentUser.username || '';
    }
}

function handleCheckoutSubmit(e) {
    e.preventDefault();

    if (cartItems.length === 0) {
        showToast('Your cart is empty', 'fa-triangle-exclamation');
        return;
    }

    const fullName = document.getElementById('chkFullName').value;
    const email = document.getElementById('chkEmail').value;
    const address = document.getElementById('chkAddress').value;
    const city = document.getElementById('chkCity').value;
    const zipCode = document.getElementById('chkZip').value;

    const total = cartItems.reduce((acc, item) => acc + (item.price * item.quantity), 0);
    const orderId = Math.floor(100000 + Math.random() * 900000);
    const now = new Date();
    const dateStr = now.toISOString().slice(0, 10) + ' ' + now.toTimeString().slice(0, 5);

    const newOrder = {
        id: orderId,
        username: currentUser ? currentUser.username : null,
        full_name: fullName,
        email: email,
        address: address,
        city: city,
        zip_code: zipCode,
        total_amount: total,
        status: 'Processing',
        created_at: dateStr,
        items: cartItems.map(item => ({
            product_name: item.name,
            price: item.price,
            quantity: item.quantity,
            image_url: item.image_url
        }))
    };

    const orders = JSON.parse(localStorage.getItem('nexus_orders') || '[]');
    orders.unshift(newOrder);
    localStorage.setItem('nexus_orders', JSON.stringify(orders));

    // Clear Cart
    cartItems = [];
    saveCart();
    loadCart();

    closeModal('checkoutModal');
    showToast(`Order #${orderId} placed successfully!`, 'fa-circle-check');

    if (currentUser) {
        setTimeout(openOrdersModal, 500);
    }
}

// ==========================================
// USER AUTHENTICATION
// ==========================================
function openAuthModal() {
    if (currentUser) {
        if (confirm(`Logout from ${currentUser.username}?`)) {
            currentUser = null;
            localStorage.removeItem('nexus_current_user');
            showToast('Logged out successfully');
            checkAuthStatus();
        }
    } else {
        openModal('authModal');
    }
}

function switchAuthTab(tab) {
    if (tab === 'login') {
        document.getElementById('loginTab').classList.add('active');
        document.getElementById('registerTab').classList.remove('active');
        document.getElementById('loginForm').style.display = 'block';
        document.getElementById('registerForm').style.display = 'none';
    } else {
        document.getElementById('registerTab').classList.add('active');
        document.getElementById('loginTab').classList.remove('active');
        document.getElementById('registerForm').style.display = 'block';
        document.getElementById('loginForm').style.display = 'none';
    }
}

function handleLoginSubmit(e) {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value.trim();

    const users = JSON.parse(localStorage.getItem('nexus_users') || '[]');
    const user = users.find(u => u.username.toLowerCase() === username.toLowerCase() && u.password === password);

    if (user) {
        currentUser = { username: user.username, email: user.email };
        localStorage.setItem('nexus_current_user', JSON.stringify(currentUser));
        closeModal('authModal');
        showToast(`Welcome back, ${user.username}!`);
        checkAuthStatus();
        document.getElementById('loginForm').reset();
    } else {
        showToast('Invalid username or password', 'fa-triangle-exclamation');
    }
}

function handleRegisterSubmit(e) {
    e.preventDefault();
    const username = document.getElementById('regUsername').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    const password = document.getElementById('regPassword').value.trim();

    if (password.length < 6) {
        showToast('Password must be at least 6 characters', 'fa-triangle-exclamation');
        return;
    }

    const users = JSON.parse(localStorage.getItem('nexus_users') || '[]');
    if (users.some(u => u.username.toLowerCase() === username.toLowerCase())) {
        showToast('Username already taken', 'fa-triangle-exclamation');
        return;
    }

    const newUser = { username, email, password };
    users.push(newUser);
    localStorage.setItem('nexus_users', JSON.stringify(users));

    currentUser = { username, email };
    localStorage.setItem('nexus_current_user', JSON.stringify(currentUser));

    closeModal('authModal');
    showToast(`Account created for ${username}!`);
    checkAuthStatus();
    document.getElementById('registerForm').reset();
}

// ==========================================
// ORDERS MODAL (Order History)
// ==========================================
function openOrdersModal() {
    openModal('ordersModal');
    const container = document.getElementById('ordersList');
    if (!container) return;

    const allOrders = JSON.parse(localStorage.getItem('nexus_orders') || '[]');
    const userOrders = currentUser 
        ? allOrders.filter(o => o.username === currentUser.username || !o.username)
        : allOrders;

    if (userOrders.length === 0) {
        container.innerHTML = `
            <div class="empty-cart" style="padding: 2rem;">
                <i class="fa-solid fa-receipt"></i>
                <h3>No past orders</h3>
                <p>Place an order to see your purchase history here.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = userOrders.map(o => `
        <div class="order-card">
            <div class="order-card-header">
                <div>
                    <strong>Order #${o.id}</strong>
                    <div style="font-size: 0.8rem; color: var(--text-muted);">${o.created_at}</div>
                </div>
                <span class="order-badge">${o.status}</span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                ${o.items.map(item => `
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                        <span>${item.quantity}x ${item.product_name}</span>
                        <span style="color: var(--primary);">${formatINR(item.price * item.quantity)}</span>
                    </div>
                `).join('')}
            </div>
            <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid var(--border-color); display: flex; justify-content: space-between; font-weight: bold;">
                <span>Total Amount:</span>
                <span>${formatINR(o.total_amount)}</span>
            </div>
        </div>
    `).join('');
}

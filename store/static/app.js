// State Management
let currentCategory = 'all';
let searchQuery = '';
let cartItems = [];
let currentUser = null;

document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
    loadCategories();
    loadProducts();
    loadCart();
});

// Toast Notifications
function showToast(message, icon = 'fa-circle-check') {
    const container = document.getElementById('toastContainer');
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
async function checkAuthStatus() {
    try {
        const res = await fetch('/api/auth/me/');
        const data = await res.json();
        if (data.authenticated) {
            currentUser = data.user;
            document.getElementById('userBtnText').innerText = currentUser.username;
            document.getElementById('ordersBtn').style.display = 'inline-flex';
        } else {
            currentUser = null;
            document.getElementById('userBtnText').innerText = 'Sign In';
            document.getElementById('ordersBtn').style.display = 'none';
        }
    } catch (err) {
        console.error('Error checking auth:', err);
    }
}

// Load Categories
async function loadCategories() {
    try {
        const res = await fetch('/api/categories/');
        const data = await res.json();
        const container = document.getElementById('categoriesBar');
        
        let html = `
            <button class="category-chip ${currentCategory === 'all' ? 'active' : ''}" onclick="filterCategory('all')">
                <i class="fa-solid fa-layer-group"></i> All
            </button>
        `;
        
        data.categories.forEach(cat => {
            html += `
                <button class="category-chip ${currentCategory === cat.slug ? 'active' : ''}" onclick="filterCategory('${cat.slug}')">
                    <i class="fa-solid ${cat.icon}"></i> ${cat.name}
                </button>
            `;
        });
        container.innerHTML = html;
    } catch (err) {
        console.error('Error loading categories:', err);
    }
}

// Load Products
async function loadProducts() {
    const grid = document.getElementById('productGrid');
    grid.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p>Loading products catalog...</p>
        </div>
    `;

    try {
        let url = `/api/products/?category=${currentCategory}`;
        if (searchQuery) url += `&search=${encodeURIComponent(searchQuery)}`;

        const res = await fetch(url);
        const data = await res.json();

        if (data.products.length === 0) {
            grid.innerHTML = `
                <div class="empty-cart" style="grid-column: 1/-1; padding: 4rem;">
                    <i class="fa-solid fa-box-open"></i>
                    <h3>No products found</h3>
                    <p>Try searching for something else or clearing filters.</p>
                </div>
            `;
            return;
        }

        grid.innerHTML = data.products.map(p => {
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
                            <span class="current-price">$${p.price.toFixed(2)}</span>
                            ${p.original_price ? `<span class="old-price">$${p.original_price.toFixed(2)}</span>` : ''}
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
    } catch (err) {
        console.error('Error fetching products:', err);
    }
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
    clearBtn.style.display = searchQuery ? 'inline-block' : 'none';
    if (e.key === 'Enter' || searchQuery === '') {
        loadProducts();
    }
}

function clearSearch() {
    document.getElementById('searchInput').value = '';
    searchQuery = '';
    document.getElementById('clearSearchBtn').style.display = 'none';
    loadProducts();
}

function scrollToShop() {
    document.getElementById('shop').scrollIntoView({ behavior: 'smooth' });
}

// CART MANAGEMENT
async function loadCart() {
    try {
        const res = await fetch('/api/cart/');
        const data = await res.json();
        cartItems = data.items;

        const countBadge = document.getElementById('cartBadge');
        const itemsContainer = document.getElementById('cartItemsContainer');
        const checkoutBtn = document.getElementById('checkoutTriggerBtn');

        const totalQty = cartItems.reduce((acc, i) => acc + i.quantity, 0);
        countBadge.innerText = totalQty;

        if (cartItems.length === 0) {
            itemsContainer.innerHTML = `
                <div class="empty-cart">
                    <i class="fa-solid fa-basket-shopping"></i>
                    <h3>Your cart is empty</h3>
                    <p>Add some sleek tech products to get started!</p>
                </div>
            `;
            document.getElementById('cartSubtotal').innerText = '$0.00';
            document.getElementById('cartTotal').innerText = '$0.00';
            checkoutBtn.disabled = true;
            return;
        }

        checkoutBtn.disabled = false;
        itemsContainer.innerHTML = cartItems.map(item => `
            <div class="cart-item">
                <img src="${item.image_url}" alt="${item.name}">
                <div class="cart-item-info">
                    <h4>${item.name}</h4>
                    <span class="cart-item-price">$${item.price.toFixed(2)}</span>
                </div>
                <div class="qty-controls">
                    <button class="qty-btn" onclick="updateCartQty(${item.id}, ${item.quantity - 1})">-</button>
                    <span class="qty-val">${item.quantity}</span>
                    <button class="qty-btn" onclick="updateCartQty(${item.id}, ${item.quantity + 1})">+</button>
                </div>
            </div>
        `).join('');

        document.getElementById('cartSubtotal').innerText = `$${data.total.toFixed(2)}`;
        document.getElementById('cartTotal').innerText = `$${data.total.toFixed(2)}`;
    } catch (err) {
        console.error('Error loading cart:', err);
    }
}

async function addToCart(productId) {
    try {
        const res = await fetch('/api/cart/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId, quantity: 1 })
        });
        const data = await res.json();
        showToast('Item added to cart!', 'fa-bag-shopping');
        loadCart();
    } catch (err) {
        console.error('Error adding to cart:', err);
    }
}

async function updateCartQty(itemId, quantity) {
    try {
        await fetch('/api/cart/', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ item_id: itemId, quantity })
        });
        loadCart();
    } catch (err) {
        console.error('Error updating cart quantity:', err);
    }
}

function toggleCartDrawer() {
    document.getElementById('cartDrawer').classList.toggle('active');
    document.getElementById('cartOverlay').classList.toggle('active');
}

// MODAL CONTROL
function openModal(id) {
    document.getElementById(id).classList.add('active');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}

// PRODUCT QUICK VIEW MODAL
async function openProductModal(productId) {
    openModal('productModal');
    const modalBody = document.getElementById('productModalBody');
    modalBody.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p>Loading details...</p>
        </div>
    `;

    try {
        const res = await fetch(`/api/products/${productId}/`);
        const data = await res.json();
        const p = data.product;

        modalBody.innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: center;">
                <div style="border-radius: var(--radius-md); overflow: hidden; border: 1px solid var(--border-color);">
                    <img src="${p.image_url}" alt="${p.name}" style="width: 100%; height: 320px; object-fit: cover;">
                </div>
                <div>
                    <span class="product-tag" style="position: static; display: inline-block; margin-bottom: 0.8rem;">${p.category_name}</span>
                    <h2 style="font-size: 1.8rem; margin-bottom: 0.5rem;">${p.name}</h2>
                    <div class="product-rating" style="margin-bottom: 1rem;">
                        <i class="fa-solid fa-star"></i> <strong>${p.rating}</strong> <span>(${p.reviews_count} reviews)</span>
                    </div>
                    <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 1.5rem;">${p.description}</p>
                    <div style="font-size: 2rem; font-weight: 800; color: var(--text-main); margin-bottom: 1.5rem;">
                        $${p.price.toFixed(2)}
                    </div>
                    <button class="btn btn-primary btn-block" onclick="addToCart(${p.id}); closeModal('productModal');">
                        <i class="fa-solid fa-cart-plus"></i> Add to Cart Now
                    </button>
                </div>
            </div>
        `;
    } catch (err) {
        console.error(err);
    }
}

// CHECKOUT FORM
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

async function handleCheckoutSubmit(e) {
    e.preventDefault();
    const payload = {
        full_name: document.getElementById('chkFullName').value,
        email: document.getElementById('chkEmail').value,
        address: document.getElementById('chkAddress').value,
        city: document.getElementById('chkCity').value,
        zip_code: document.getElementById('chkZip').value,
    };

    try {
        const res = await fetch('/api/checkout/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (res.ok) {
            closeModal('checkoutModal');
            showToast(`Order #${data.order_id} placed successfully!`, 'fa-circle-check');
            loadCart();
            if (currentUser) openOrdersModal();
        } else {
            showToast(data.error || 'Checkout failed', 'fa-triangle-exclamation');
        }
    } catch (err) {
        console.error('Checkout error:', err);
    }
}

// AUTHENTICATION MODAL
function openAuthModal() {
    if (currentUser) {
        // Logout if clicked while logged in
        if (confirm(`Logout from ${currentUser.username}?`)) {
            fetch('/api/auth/logout/', { method: 'POST' }).then(() => {
                showToast('Logged out successfully');
                checkAuthStatus();
            });
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

async function handleLoginSubmit(e) {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const res = await fetch('/api/auth/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (res.ok) {
            closeModal('authModal');
            showToast(`Welcome back, ${username}!`);
            checkAuthStatus();
            loadCart();
        } else {
            showToast(data.error || 'Login failed', 'fa-triangle-exclamation');
        }
    } catch (err) {
        console.error(err);
    }
}

async function handleRegisterSubmit(e) {
    e.preventDefault();
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;

    try {
        const res = await fetch('/api/auth/register/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        const data = await res.json();
        if (res.ok) {
            closeModal('authModal');
            showToast(`Account created for ${username}!`);
            checkAuthStatus();
            loadCart();
        } else {
            showToast(data.error || 'Registration failed', 'fa-triangle-exclamation');
        }
    } catch (err) {
        console.error(err);
    }
}

// ORDERS MODAL
async function openOrdersModal() {
    openModal('ordersModal');
    const container = document.getElementById('ordersList');
    container.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p>Fetching your orders...</p>
        </div>
    `;

    try {
        const res = await fetch('/api/orders/');
        const data = await res.json();

        if (data.orders.length === 0) {
            container.innerHTML = `
                <div class="empty-cart" style="padding: 2rem;">
                    <i class="fa-solid fa-receipt"></i>
                    <h3>No past orders</h3>
                    <p>Place an order to see your purchase history here.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = data.orders.map(o => `
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
                            <span style="color: var(--primary);">$${(item.price * item.quantity).toFixed(2)}</span>
                        </div>
                    `).join('')}
                </div>
                <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid var(--border-color); display: flex; justify-content: space-between; font-weight: bold;">
                    <span>Total Amount:</span>
                    <span>$${o.total_amount.toFixed(2)}</span>
                </div>
            </div>
        `).join('');
    } catch (err) {
        console.error(err);
    }
}

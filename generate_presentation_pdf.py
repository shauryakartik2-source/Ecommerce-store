import os
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_PATH = "NEXUS_Store_Internship_Presentation.pdf"

# Slide Canvas for background and footer
class SlideCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_slide_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_slide_decorations(self, total_pages):
        w, h = landscape(A4)
        
        # Background gradient or dark solid
        self.saveState()
        self.setFillColor(colors.HexColor("#090d16"))
        self.rect(0, 0, w, h, fill=1, stroke=0)
        
        # Subtle top accent bar
        self.setFillColor(colors.HexColor("#6366f1"))
        self.rect(0, h - 5, w, 5, fill=1, stroke=0)
        
        # Subtle glowing circles/shapes on background
        self.setFillColor(colors.HexColor("#1e1b4b"), alpha=0.3)
        self.circle(w - 60, h - 60, 120, fill=1, stroke=0)
        self.circle(80, 80, 100, fill=1, stroke=0)
        
        # Footer Bar
        self.setStrokeColor(colors.HexColor("#1e293b"))
        self.setLineWidth(1)
        self.line(40, 32, w - 40, 32)
        
        # Footer text
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#6366f1"))
        self.drawString(40, 18, "CODEALPHA INTERNSHIP PROJECT")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#94a3b8"))
        self.drawString(220, 18, "NEXUS E-Commerce Store | Shaurya Kartik (Roorkee Institute of Technology)")
        
        page_num_str = f"Slide {self._pageNumber} of {total_pages}"
        self.drawRightString(w - 40, 18, page_num_str)
        
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=landscape(A4),
        leftMargin=45,
        rightMargin=45,
        topMargin=35,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_main = ParagraphStyle(
        'TitleMain',
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#ffffff"),
        alignment=0
    )

    title_sub = ParagraphStyle(
        'TitleSub',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#818cf8"),
        alignment=0
    )

    slide_header = ParagraphStyle(
        'SlideHeader',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#ffffff")
    )

    slide_category = ParagraphStyle(
        'SlideCat',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#10b981")
    )

    body_text = ParagraphStyle(
        'BodyDark',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#cbd5e1")
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#ffffff")
    )

    bullet_item = ParagraphStyle(
        'BulletItem',
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#cbd5e1"),
        leftIndent=15
    )

    card_title = ParagraphStyle(
        'CardTitle',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#a5b4fc")
    )

    card_text = ParagraphStyle(
        'CardText',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#94a3b8")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#e2e8f0")
    )

    table_header = ParagraphStyle(
        'TableHead',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#67e8f9")
    )

    story = []

    def slide_title(category, title):
        return [
            Paragraph(category.upper(), slide_category),
            Spacer(1, 2),
            Paragraph(title, slide_header),
            Spacer(1, 14)
        ]

    # -------------------------------------------------------------
    # SLIDE 1: COVER SLIDE
    # -------------------------------------------------------------
    story.append(Spacer(1, 25))
    story.append(Paragraph("CODEALPHA FULL STACK / WEB DEV INTERNSHIP", slide_category))
    story.append(Spacer(1, 6))
    story.append(Paragraph("NEXUS E-Commerce Store", title_main))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Modern Glassmorphic Client-Side E-Commerce Web Application", title_sub))
    story.append(Spacer(1, 20))

    # Meta card table
    cover_data = [
        [
            Paragraph("<b>Presented By:</b><br/>Shaurya Kartik<br/>B.Tech - Computer Science & Engineering", body_text),
            Paragraph("<b>Institution:</b><br/>Roorkee Institute of Technology, Roorkee<br/>Affiliated to VMSB UTU, Dehradun", body_text),
            Paragraph("<b>Internship Organization:</b><br/>CodeAlpha (Virtual Internship Program)<br/>Recognized by Ministry of Corporate Affairs, GoI", body_text),
            Paragraph("<b>Project Period:</b><br/>August 2026 – September 2026<br/>Task 1: Simple E-Commerce Store", body_text)
        ]
    ]
    t_cover = Table(cover_data, colWidths=[185, 185, 195, 185])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#312e81")),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor("#1e293b")),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 25))

    p_badge = Paragraph(
        "<b>Key Highlights:</b> 100% Pure HTML5, CSS3 & Vanilla JavaScript | Zero-Server Dependency | "
        "LocalStorage Persistence | Full INR (₹) Currency Localization | Mobile-First Responsive Design",
        ParagraphStyle('BadgeText', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor("#38bdf8"))
    )
    t_badge = Table([[p_badge]], colWidths=[750])
    t_badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1e1b4b")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#4338ca")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(t_badge)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 2: PROJECT OVERVIEW & PROBLEM STATEMENT
    # -------------------------------------------------------------
    story.extend(slide_title("Executive Summary", "1. Project Overview & Problem Statement"))
    
    overview_left = [
        Paragraph("<b>The Objective:</b>", body_bold),
        Spacer(1, 4),
        Paragraph("To build a high-performance, visually stunning e-commerce web application that delivers a frictionless shopping experience directly in the browser with zero deployment friction.", body_text),
        Spacer(1, 10),
        Paragraph("<b>The Problem Addressed:</b>", body_bold),
        Spacer(1, 4),
        Paragraph("• Most traditional demo projects require complex backend runtime setups (databases, servers, pip/npm installs) that fail during quick viva or classroom demos.<br/>"
                  "• Conventional basic student web pages lack modern UX expectations such as live instant search, category filtering, persistent carts, and checkout confirmation.<br/>"
                  "• Mobile responsiveness is often an afterthought, resulting in broken layouts on smartphones.", body_text)
    ]

    overview_right = [
        Paragraph("<b>The Solution — NEXUS STORE:</b>", body_bold),
        Spacer(1, 4),
        Paragraph("• <b>Pure Client-Side Architecture:</b> 100% executable by opening <code>index.html</code> in any modern browser.<br/>"
                  "• <b>Full E-Commerce Lifecycle:</b> Catalog browsing ➔ Real-time filtering ➔ Quick View ➔ Interactive Cart Drawer ➔ Checkout Form ➔ Order History ➔ User Authentication.<br/>"
                  "• <b>Browser-Native State Persistence:</b> Uses HTML5 Web Storage (<code>localStorage</code>) to emulate an enterprise database.<br/>"
                  "• <b>Indian Rupee (₹) Locale:</b> Realistic INR pricing and formatting.", body_text),
        Spacer(1, 10),
        Paragraph("<b>Deployment Readiness:</b>", body_bold),
        Spacer(1, 4),
        Paragraph("Directly hosted and runnable via GitHub Pages with zero cloud hosting costs.", body_text)
    ]

    t_overview = Table([[overview_left, overview_right]], colWidths=[370, 380])
    t_overview.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#0f172a")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#111827")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1e293b")),
        ('PADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(t_overview)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 3: SYSTEM ARCHITECTURE & DATA FLOW
    # -------------------------------------------------------------
    story.extend(slide_title("System Design", "2. Architecture & Data Flow"))

    arch_cards = [
        [
            Paragraph("<b>1. Presentation Layer (UI)</b>", card_title),
            Paragraph("<b>2. Business Logic Layer</b>", card_title),
            Paragraph("<b>3. Persistence Layer (DB)</b>", card_title)
        ],
        [
            Paragraph("• Semantic HTML5 Elements<br/>"
                      "• Dark Glassmorphism CSS3<br/>"
                      "• Responsive Flexbox & CSS Grid<br/>"
                      "• Keyframe Transitions & Modals<br/>"
                      "• Mobile Viewport Optimizations", card_text),
            Paragraph("• Vanilla JavaScript (ES6+)<br/>"
                      "• DOM Event Listeners & Rendering<br/>"
                      "• Search & Category Query Engine<br/>"
                      "• INR (₹) Financial Formatting<br/>"
                      "• Form Validation & Order Engine", card_text),
            Paragraph("• Browser <code>localStorage</code> API<br/>"
                      "• <code>nexus_products</code>: Catalog<br/>"
                      "• <code>nexus_cart</code>: Active Items<br/>"
                      "• <code>nexus_orders</code>: Placed Bills<br/>"
                      "• <code>nexus_users</code>: Auth Records", card_text)
        ]
    ]
    t_arch = Table(arch_cards, colWidths=[245, 255, 250])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#312e81")),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor("#1e293b")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 14))

    flow_box = [
        Paragraph("<b>End-to-End User Interaction Flow:</b>", body_bold),
        Spacer(1, 4),
        Paragraph("1. <b>Page Load</b> ➔ JS checks <code>localStorage</code> version ➔ Seeds default INR tech products ➔ Renders category chips & cards.<br/>"
                  "2. <b>Search/Filter</b> ➔ Immediate JS query filter on in-memory array ➔ Dynamic DOM replacement without page refresh.<br/>"
                  "3. <b>Add to Cart</b> ➔ Item serialized to <code>nexus_cart</code> ➔ Slide-out cart drawer smoothly opens ➔ Subtotal recomputed.<br/>"
                  "4. <b>Checkout</b> ➔ Multi-field shipping form validated ➔ 6-digit Order ID generated ➔ Saved to <code>nexus_orders</code> ➔ Cart flushed.<br/>"
                  "5. <b>Order History</b> ➔ Logged-in user accesses historical receipts with date, items, total, and live 'Processing' status.", body_text)
    ]
    t_flow = Table([[flow_box]], colWidths=[750])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#090d16")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1e293b")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_flow)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 4: TECH STACK BREAKDOWN
    # -------------------------------------------------------------
    story.extend(slide_title("Technology Foundation", "3. Technologies Used & Rationale"))

    tech_table_data = [
        [Paragraph("Technology", table_header), Paragraph("Role in Project", table_header), Paragraph("Key Features & Implementation Rationale", table_header)],
        [
            Paragraph("<b>HTML5</b>", table_cell),
            Paragraph("Structure & Layout", table_cell),
            Paragraph("Semantic tags (<code>&lt;nav&gt;</code>, <code>&lt;main&gt;</code>, <code>&lt;aside&gt;</code>, <code>&lt;footer&gt;</code>). Accessible modals, clean input forms, and mobile viewport meta configuration.", table_cell)
        ],
        [
            Paragraph("<b>CSS3 (Glassmorphism)</b>", table_cell),
            Paragraph("Visual Design System", table_cell),
            Paragraph("Modern dark aesthetics with <code>backdrop-filter: blur(16px)</code>, glowing borders, CSS variables, CSS Grid, smooth drawer transforms, and toast keyframe animations.", table_cell)
        ],
        [
            Paragraph("<b>Vanilla JavaScript (ES6+)</b>", table_cell),
            Paragraph("Application Logic Engine", table_cell),
            Paragraph("Zero dependencies or bloated frameworks. Employs async DOM rendering, event delegation, array map/filter/reduce pipelines, and client-side routing.", table_cell)
        ],
        [
            Paragraph("<b>LocalStorage API</b>", table_cell),
            Paragraph("Client-Side Database", table_cell),
            Paragraph("Browser-level persistent key-value store. Guarantees that carts, orders, and user logins survive page reloads and browser restarts.", table_cell)
        ],
        [
            Paragraph("<b>FontAwesome 6</b>", table_cell),
            Paragraph("Vector Iconography", table_cell),
            Paragraph("CDN-loaded SVG icons for shopping bags, star reviews, tech specs, search magnifying glass, lock icons, and user authentication.", table_cell)
        ],
        [
            Paragraph("<b>Google Fonts (Outfit)</b>", table_cell),
            Paragraph("Typography", table_cell),
            Paragraph("High-clarity geometric sans-serif typeface tailored for high-end digital tech products and e-commerce readability.", table_cell)
        ],
        [
            Paragraph("<b>Git & GitHub</b>", table_cell),
            Paragraph("Version Control & Cloud", table_cell),
            Paragraph("Full Git version history, remote tracking, and instant zero-cost static hosting via GitHub Pages.", table_cell)
        ]
    ]
    t_tech = Table(tech_table_data, colWidths=[140, 150, 460])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e1b4b")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#312e81")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#1e293b")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_tech)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 5: MODULE 1 — PRODUCT CATALOG & DISCOVERY
    # -------------------------------------------------------------
    story.extend(slide_title("Feature Showcase", "4. Product Catalog & Live Discovery"))

    col1 = [
        Paragraph("<b>1. Multi-Category Filtering</b>", card_title),
        Spacer(1, 4),
        Paragraph("• Four dedicated categories: <i>Audio & Sound</i>, <i>Smart Wearables</i>, <i>Computing & Tech</i>, and <i>Accessories</i>.<br/>"
                  "• Interactive filter chips highlight active states dynamically.<br/>"
                  "• 'All' button instantly clears filters to show the full collection.<br/>"
                  "• Real-time array filtering runs in sub-millisecond execution time.", card_text),
        Spacer(1, 10),
        Paragraph("<b>2. Instant Keyword Search</b>", card_title),
        Spacer(1, 4),
        Paragraph("• Live <code>onkeyup</code> search bar with instant query matching.<br/>"
                  "• Matches keywords across product titles AND detailed descriptions.<br/>"
                  "• Integrated clear search button ('✕') for rapid reset.<br/>"
                  "• Displays friendly empty state when no products match.", card_text)
    ]

    col2 = [
        Paragraph("<b>3. Rich Product Cards</b>", card_title),
        Spacer(1, 4),
        Paragraph("• High-resolution product imagery with hover zoom scale effect.<br/>"
                  "• Dynamic discount badge (e.g. <code>-20%</code>) auto-calculated from original vs current price.<br/>"
                  "• Star ratings with real review count displays.<br/>"
                  "• Price display rendered in Indian Rupees (<code>₹</code>) with locale commas.", card_text),
        Spacer(1, 10),
        Paragraph("<b>4. Quick-View Modal Window</b>", card_title),
        Spacer(1, 4),
        Paragraph("• Eye icon trigger opens modal overlay with blurred backdrop.<br/>"
                  "• Displays full expanded tech specifications and high-res preview.<br/>"
                  "• Direct 'Add to Cart Now' action from inside modal.<br/>"
                  "• Responsive 2-column layout that shifts to vertical stack on mobile.", card_text)
    ]

    t_mod1 = Table([[col1, col2]], colWidths=[370, 380])
    t_mod1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#0f172a")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#111827")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1e293b")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_mod1)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 6: MODULE 2 — SHOPPING CART & FINANCIAL CALCULATION
    # -------------------------------------------------------------
    story.extend(slide_title("Feature Showcase", "5. Interactive Shopping Cart & Price Engine"))

    col_cart1 = [
        Paragraph("<b>Slide-Out Cart Drawer Architecture</b>", card_title),
        Spacer(1, 4),
        Paragraph("• Fixed overlay drawer that glides smoothly from the right edge with cubic-bezier transition.<br/>"
                  "• Real-time badge counter on navbar bag icon indicates total quantity of items.<br/>"
                  "• Interactive quantity stepper controls (<code>+</code> / <code>-</code>) per cart item.<br/>"
                  "• Automatically purges item from cart when quantity is decremented to 0.<br/>"
                  "• Empty state banner with clear call-to-action when cart has no items.", card_text),
        Spacer(1, 10),
        Paragraph("<b>LocalStorage State Sync</b>", card_title),
        Spacer(1, 4),
        Paragraph("• Every add, update, or delete operation immediately invokes <code>saveCart()</code>.<br/>"
                  "• Cart contents persist across browser tabs, page refreshes, and computer reboots.", card_text)
    ]

    col_cart2 = [
        Paragraph("<b>Indian Rupee (₹) Pricing Engine</b>", card_title),
        Spacer(1, 4),
        Paragraph("• All prices calculated using standard Indian number formatting via custom <code>formatINR()</code> utility:<br/>"
                  "&nbsp;&nbsp;<code>return '₹' + Number(amt).toLocaleString('en-IN', { ... });</code><br/>"
                  "• Automatically formats large figures with proper Indian comma separators (e.g. <code>₹2,999.00</code>).<br/>"
                  "• Calculates dynamic subtotal and final checkout total.<br/>"
                  "• Shows free promotional shipping badge for internship demonstration.", card_text),
        Spacer(1, 10),
        Paragraph("<b>Sample Catalog Pricing:</b>", card_title),
        Spacer(1, 4),
        Paragraph("• AeroPulse ANC Headphones: <b>₹1,999.00</b> (Was ₹2,499)<br/>"
                  "• Titanium Apex Pro Smartwatch: <b>₹2,999.00</b> (Was ₹3,499)<br/>"
                  "• Mechanical CyberDeck Keyboard: <b>₹1,299.00</b> (Was ₹1,599)<br/>"
                  "• SonicBass Mini Speaker: <b>₹599.00</b> | Mouse: <b>₹899.00</b>", card_text)
    ]

    t_mod2 = Table([[col_cart1, col_cart2]], colWidths=[370, 380])
    t_mod2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#0f172a")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#111827")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1e293b")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_mod2)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 7: MODULE 3 — CHECKOUT & ORDER MANAGEMENT
    # -------------------------------------------------------------
    story.extend(slide_title("Feature Showcase", "6. Checkout Process & Order Tracking"))

    col_chk1 = [
        Paragraph("<b>1. Multi-Field Shipping Form</b>", card_title),
        Spacer(1, 4),
        Paragraph("• Full Name, Email, Shipping Address, City, and Postal Code.<br/>"
                  "• Client-side HTML5 input validation prevents blank submissions.<br/>"
                  "• Auto-populates logged-in user's name and email automatically.<br/>"
                  "• Order summary breakdown displays total amount before placing order.", card_text),
        Spacer(1, 10),
        Paragraph("<b>2. Unique Order ID Generation</b>", card_title),
        Spacer(1, 4),
        Paragraph("• Generates a cryptographically random 6-digit bill reference number:<br/>"
                  "&nbsp;&nbsp;<code>const orderId = Math.floor(100000 + Math.random() * 900000);</code><br/>"
                  "• Records exact ISO timestamp (date & time) for verification.<br/>"
                  "• Stores complete snapshot of purchased items and prices.", card_text)
    ]

    col_chk2 = [
        Paragraph("<b>3. Order History Dashboard ('My Orders')</b>", card_title),
        Spacer(1, 4),
        Paragraph("• Dedicated modal accessible via navbar button.<br/>"
                  "• Lists historical purchase receipts in reverse-chronological order.<br/>"
                  "• Displays live status badge: <font color='#10b981'><b>Processing</b></font>.<br/>"
                  "• Itemized breakdown with item counts, thumbnails, and total bill.", card_text),
        Spacer(1, 10),
        Paragraph("<b>4. Instant User Feedback (Toast Notifications)</b>", card_title),
        Spacer(1, 4),
        Paragraph("• Non-blocking animated toast alerts slide in from the bottom right.<br/>"
                  "• Success notifications on Add to Cart, Order Placed, Login, and Logout.<br/>"
                  "• Auto-dismissing after 3 seconds with smooth fade-out animation.", card_text)
    ]

    t_mod3 = Table([[col_chk1, col_chk2]], colWidths=[370, 380])
    t_mod3.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#0f172a")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#111827")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1e293b")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_mod3)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 8: MODULE 4 — AUTHENTICATION & USER MANAGEMENT
    # -------------------------------------------------------------
    story.extend(slide_title("Feature Showcase", "7. User Authentication & Session Handling"))

    auth_cards = [
        [
            Paragraph("<b>User Registration (Sign Up)</b>", card_title),
            Paragraph("<b>User Authentication (Sign In)</b>", card_title),
            Paragraph("<b>Session Persistence</b>", card_title)
        ],
        [
            Paragraph("• User supplies username, email, and password (min 6 chars).<br/>"
                      "• Verifies username uniqueness against <code>nexus_users</code>.<br/>"
                      "• Registers new user and signs in immediately.<br/>"
                      "• Displays personalized toast alert.", card_text),
            Paragraph("• Case-insensitive username lookup with password verification.<br/>"
                      "• Error toast on invalid credentials.<br/>"
                      "• Switches dynamically between Sign In and Sign Up tabs in modal.<br/>"
                      "• Updates Navbar to show user's name.", card_text),
            Paragraph("• Active session stored in <code>nexus_current_user</code>.<br/>"
                      "• Navbar reveals 'My Orders' button when authenticated.<br/>"
                      "• Clicking user name prompts quick logout confirmation.<br/>"
                      "• Guest checkout remains fully supported!", card_text)
        ]
    ]
    t_auth = Table(auth_cards, colWidths=[245, 255, 250])
    t_auth.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#312e81")),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor("#1e293b")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_auth)
    story.append(Spacer(1, 14))

    guest_vs_auth = [
        Paragraph("<b>Dual-Mode Accessibility (Guest vs Logged-In User):</b>", body_bold),
        Spacer(1, 4),
        Paragraph("• <b>Guest Users:</b> Can immediately browse products, filter categories, search, add items to cart, and checkout without being forced to create an account.<br/>"
                  "• <b>Authenticated Users:</b> Get automated pre-filling of shipping forms and direct access to order history linked to their specific username.<br/>"
                  "• Demonstrates modern user-retention design where checkout barriers are minimized.", body_text)
    ]
    t_gva = Table([[guest_vs_auth]], colWidths=[750])
    t_gva.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#090d16")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1e293b")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_gva)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 9: MOBILE-FIRST & RESPONSIVE ENGINEERING
    # -------------------------------------------------------------
    story.extend(slide_title("Engineering Excellence", "8. Mobile-First & Responsive Optimizations"))

    col_mob1 = [
        Paragraph("<b>Two-Row Mobile Navbar</b>", card_title),
        Spacer(1, 4),
        Paragraph("• On screens &lt; 768px, Navbar splits cleanly into two rows:<br/>"
                  "&nbsp;&nbsp;- Row 1: Logo on left, User & Cart buttons on right.<br/>"
                  "&nbsp;&nbsp;- Row 2: Full-width search bar with magnifying glass icon.<br/>"
                  "• Follows modern standards used by Amazon, Apple, and Flipkart.", card_text),
        Spacer(1, 10),
        Paragraph("<b>Touch-Optimized Category Bar</b>", card_title),
        Spacer(1, 4),
        Paragraph("• Implements <code>-webkit-overflow-scrolling: touch</code>.<br/>"
                  "• Hidden scrollbars with horizontal kinetic swipe gestures.<br/>"
                  "• Touch manipulation tags prevent double-tap delays on buttons.", card_text)
    ]

    col_mob2 = [
        Paragraph("<b>Full-Screen Drawer & Bottom-Sheet Modals</b>", card_title),
        Spacer(1, 4),
        Paragraph("• Cart drawer slides to 100% viewport width on phones.<br/>"
                  "• Modals adapt to elegant bottom-sheets with rounded top corners.<br/>"
                  "• Form inputs locked at <code>font-size: 16px</code> to prevent unwanted iOS Safari auto-zoom behavior.<br/>"
                  "• Single-column stacked product cards with large touch targets.", card_text),
        Spacer(1, 10),
        Paragraph("<b>Mobile Browser Header Theme Integration</b>", card_title),
        Spacer(1, 4),
        Paragraph("• Configured <code>&lt;meta name='theme-color' content='#090d16'&gt;</code>.<br/>"
                  "• Mobile address bars in Chrome Android and iOS Safari blend natively with the app's dark glass background.", card_text)
    ]

    t_mob = Table([[col_mob1, col_mob2]], colWidths=[370, 380])
    t_mob.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#0f172a")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#111827")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1e293b")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_mob)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 10: CHALLENGES FACED & TECHNICAL SOLUTIONS
    # -------------------------------------------------------------
    story.extend(slide_title("Problem Solving", "9. Key Challenges Faced & Engineering Solutions"))

    challenges_data = [
        [Paragraph("Engineering Challenge", table_header), Paragraph("Root Cause / Complication", table_header), Paragraph("Adopted Technical Solution", table_header)],
        [
            Paragraph("<b>Serverless Data Persistence</b>", table_cell),
            Paragraph("Removing the Python/Django backend eliminated SQL tables for storing carts and orders.", table_cell),
            Paragraph("Designed a normalized JSON schema layer inside HTML5 <code>localStorage</code> with auto-initialization and storage versioning.", table_cell)
        ],
        [
            Paragraph("<b>Stale LocalStorage Caches</b>", table_cell),
            Paragraph("Users who loaded older builds still had obsolete dollar prices cached in browser memory.", table_cell),
            Paragraph("Implemented <code>STORAGE_VERSION = 'nexus_v2_inr'</code> check in <code>initStorage()</code> to automatically refresh cached catalogs.", table_cell)
        ],
        [
            Paragraph("<b>Mobile Form Zoom Bug in iOS</b>", table_cell),
            Paragraph("Tapping input boxes on iPhones caused Safari to automatically zoom the page, distorting UI.", table_cell),
            Paragraph("Enforced strict <code>font-size: 16px !important</code> on all input, select, and textarea elements under <code>@media (max-width: 768px)</code>.", table_cell)
        ],
        [
            Paragraph("<b>Horizontal Viewport Overflow</b>", table_cell),
            Paragraph("Fixed-width 400px cart drawer caused horizontal scrollbars on smaller 360px mobile viewports.", table_cell),
            Paragraph("Applied <code>width: 100%; max-width: 100vw; right: -100%</code> clamped styles on mobile breakpoints.", table_cell)
        ],
        [
            Paragraph("<b>Indian Rupee Formatting</b>", table_cell),
            Paragraph("Default JavaScript formatting uses Western millions/billions commas instead of Indian lakhs.", table_cell),
            Paragraph("Created custom <code>formatINR()</code> using <code>toLocaleString('en-IN')</code> for authentic Indian Rupee currency representations.", table_cell)
        ]
    ]
    t_chal = Table(challenges_data, colWidths=[180, 260, 310])
    t_chal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e1b4b")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#312e81")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#1e293b")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_chal)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 11: REPOSITORY STRUCTURE & LIVE DEPLOYMENT
    # -------------------------------------------------------------
    story.extend(slide_title("Codebase & Delivery", "10. Repository Structure & Deployment"))

    col_repo1 = [
        Paragraph("<b>Minimalist Zero-Dependency Repository:</b>", card_title),
        Spacer(1, 6),
        Paragraph("<code>CodeAlpha_ECommerceStore/<br/>"
                  "├── index.html&nbsp;&nbsp;&nbsp;&nbsp;# Semantic Single-Page Application<br/>"
                  "├── styles.css&nbsp;&nbsp;&nbsp;&nbsp;# Full Glassmorphic Design System<br/>"
                  "├── app.js&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Client State, Logic & DB Engine<br/>"
                  "└── README.md&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Complete Documentation & Guide</code>", body_text),
        Spacer(1, 12),
        Paragraph("<b>Why this structure is optimal:</b>", body_bold),
        Spacer(1, 4),
        Paragraph("• Zero installation overhead — runs instantaneously on double click.<br/>"
                  "• Clean separation of structure, aesthetics, and business logic.<br/>"
                  "• Extremely lightweight bundle size (~50 KB total) guarantees near-instant load speeds.", body_text)
    ]

    col_repo2 = [
        Paragraph("<b>GitHub Repository & Deployment:</b>", card_title),
        Spacer(1, 6),
        Paragraph("<b>Official GitHub Repo:</b><br/>"
                  "<font color='#38bdf8'><u>https://github.com/shauryakartik2-source/Ecommerce-store</u></font>", body_text),
        Spacer(1, 10),
        Paragraph("<b>GitHub Pages Deployment Workflow:</b>", body_bold),
        Spacer(1, 4),
        Paragraph("1. Repository pushed to GitHub main branch.<br/>"
                  "2. In GitHub Settings ➔ Pages ➔ Source: 'Deploy from a branch'.<br/>"
                  "3. Branch set to <code>main</code> and folder to <code>/ (root)</code>.<br/>"
                  "4. Within 30 seconds, the site is live on global CDN with free SSL certificate!", body_text),
        Spacer(1, 10),
        Paragraph("<b>Verification & Git Status:</b>", body_bold),
        Spacer(1, 4),
        Paragraph("All commits verified with clean working tree, untracked pycache purged, and synced with <code>origin/main</code>.", body_text)
    ]

    t_repo = Table([[col_repo1, col_repo2]], colWidths=[370, 380])
    t_repo.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#0f172a")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#111827")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1e293b")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_repo)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 12: CONCLUSION, LEARNINGS & FUTURE SCOPE
    # -------------------------------------------------------------
    story.extend(slide_title("Final Assessment", "11. Conclusion, Learnings & Future Roadmap"))

    concl_col1 = [
        Paragraph("<b>Key Internship Learnings:</b>", card_title),
        Spacer(1, 4),
        Paragraph("• <b>Deep DOM & Event Handling:</b> Mastered vanilla event delegation, dynamic template rendering, and modal controllers.<br/>"
                  "• <b>Modern CSS Architecture:</b> Built an end-to-end design system using glassmorphic backdrops, CSS variables, and fluid responsive grids.<br/>"
                  "• <b>Client-Side State Modeling:</b> Learned how to design robust, persistent multi-model state architectures using the Web Storage API.<br/>"
                  "• <b>Mobile User Experience:</b> Designed adaptive layouts that gracefully transition between phone, tablet, and widescreen layouts.", body_text),
        Spacer(1, 10),
        Paragraph("<b>Personal Growth:</b>", card_title),
        Spacer(1, 4),
        Paragraph("Developed self-reliance in building production-quality web applications from ground up with clean, maintainable code standards.", body_text)
    ]

    concl_col2 = [
        Paragraph("<b>Future Roadmap & Enhancements:</b>", card_title),
        Spacer(1, 4),
        Paragraph("• <b>Payment Gateway Integration:</b> Connect Razorpay or Stripe API for real online UPI, Card, and Netbanking transactions.<br/>"
                  "• <b>Progressive Web App (PWA):</b> Add service workers and manifest for offline browsing and home-screen app installation.<br/>"
                  "• <b>Backend Microservice (Optional):</b> Connect Python Django REST or Node.js server for cloud sync and admin order fulfillment.<br/>"
                  "• <b>User Reviews & Ratings:</b> Allow customer feedback and product rating submission directly in the browser.", body_text),
        Spacer(1, 10),
        Paragraph("<b>Acknowledgment:</b>", card_title),
        Spacer(1, 4),
        Paragraph("Sincere thanks to <b>CodeAlpha</b> and <b>Roorkee Institute of Technology</b> faculty for their continuous mentorship and support.", body_text)
    ]

    t_concl = Table([[concl_col1, concl_col2]], colWidths=[370, 380])
    t_concl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#0f172a")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#111827")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1e293b")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_concl)
    story.append(Spacer(1, 16))

    # Thank you bar
    thank_you_box = [
        Paragraph("<font size='14'><b>THANK YOU!</b></font>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                  "<b>Shaurya Kartik</b> | B.Tech CSE | Roorkee Institute of Technology | CodeAlpha Intern<br/>"
                  "Questions & Discussions are warmly welcomed.",
                  ParagraphStyle('TYText', fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#ffffff"), alignment=1))
    ]
    t_ty = Table([[thank_you_box]], colWidths=[750])
    t_ty.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#312e81")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#6366f1")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(t_ty)

    doc.build(story, canvasmaker=SlideCanvas)
    print(f"Presentation PDF successfully built at: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()

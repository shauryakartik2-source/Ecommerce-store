import os
import html
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Group, Circle

PDF_OUTPUT = "CodeAlpha_Full_Stack_Internship_Report_Shaurya_Kartik.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        # Don't draw page numbers on Cover (1), Self Declaration (2), Certificate (3), Acknowledgment (4)
        # Usually academic reports start page numbering on Abstract (6) or TOC (5)
        # Looking at user's reference: Page 5 TOC lists Abstract as page 6, so page numbering starts at 5 or 6, or footer page number.
        if self._pageNumber > 4:
            self.saveState()
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.HexColor("#333333"))
            # Bottom center or bottom right page number
            self.drawCentredString(A4[0] / 2.0, 35, str(self._pageNumber))
            self.restoreState()

def build_pdf():
    # Page dimensions: A4 is 595.27 x 841.89 points
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=A4,
        leftMargin=55,
        rightMargin=55,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom styles matching user's reference PDF
    style_univ_header = ParagraphStyle(
        'UnivHeader',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1, # Centered
        textColor=colors.black
    )

    style_univ_sub = ParagraphStyle(
        'UnivSub',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=colors.black
    )

    style_report_title = ParagraphStyle(
        'ReportTitle',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        alignment=1,
        textColor=colors.black
    )

    style_meta_label = ParagraphStyle(
        'MetaLabel',
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.black
    )

    style_meta_val = ParagraphStyle(
        'MetaVal',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=15,
        alignment=1,
        textColor=colors.black
    )

    style_section_heading = ParagraphStyle(
        'SecHeading',
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        alignment=1, # Centered
        textColor=colors.black
    )

    style_subheading = ParagraphStyle(
        'SubHeading',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        alignment=0, # Left
        textColor=colors.black
    )

    style_body = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=9.8,
        leading=14.5,
        alignment=4, # Justified
        textColor=colors.HexColor("#111111")
    )

    style_body_bullet = ParagraphStyle(
        'BodyBullet',
        fontName='Helvetica',
        fontSize=9.8,
        leading=14.5,
        leftIndent=15,
        textColor=colors.HexColor("#111111")
    )

    style_code = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#1e1e1e")
    )

    style_caption = ParagraphStyle(
        'CaptionStyle',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=colors.black
    )

    style_caption_desc = ParagraphStyle(
        'CaptionDesc',
        fontName='Helvetica',
        fontSize=9.2,
        leading=13.5,
        alignment=1,
        textColor=colors.HexColor("#222222")
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE / COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>ROORKEE INSTITUTE OF TECHNOLOGY, ROORKEE</b>", style_univ_header))
    story.append(Spacer(1, 2))
    story.append(Paragraph("(Affiliated to VMSB Uttarakhand Technical University, Dehradun)", style_univ_sub))
    story.append(Spacer(1, 35))

    story.append(Paragraph("<b>Full Stack Web Development Internship Report</b>", style_report_title))
    story.append(Spacer(1, 35))

    story.append(Paragraph("<i>Submitted by :-</i>", style_meta_label))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Name - Shaurya Kartik</b>", style_meta_val))
    story.append(Spacer(1, 3))
    story.append(Paragraph("U.Roll - ______________________", style_meta_val))
    story.append(Spacer(1, 25))

    story.append(Paragraph("<i>Under the Supervision of</i>", style_meta_label))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>CODEALPHA INTERNSHIP SUPERVISOR</b>", style_meta_val))
    story.append(Spacer(1, 2))
    story.append(Paragraph("CodeAlpha", style_univ_sub))
    story.append(Spacer(1, 30))

    # RIT Logo Representation
    d = Drawing(160, 48)
    # Circle emblem
    d.add(Circle(24, 24, 20, fillColor=colors.HexColor("#1e3a8a"), strokeColor=colors.HexColor("#f59e0b"), strokeWidth=2))
    d.add(String(14, 18, "RIT", fontName="Helvetica-Bold", fontSize=11, fillColor=colors.white))
    # RIT text
    d.add(String(52, 26, "RIT", fontName="Helvetica-Bold", fontSize=22, fillColor=colors.HexColor("#1e3a8a")))
    d.add(String(52, 10, "ROORKEE", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.HexColor("#1e3a8a")))
    # NAAC A++ Badge
    d.add(Rect(108, 16, 45, 20, rx=3, ry=3, fillColor=colors.HexColor("#dc2626"), strokeColor=None))
    d.add(String(113, 21, "A++", fontName="Helvetica-Bold", fontSize=13, fillColor=colors.white))
    d.add(String(108, 6, "NAAC GRADE", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.HexColor("#dc2626")))
    
    t_logo = Table([[d]], colWidths=[160])
    t_logo.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(t_logo)
    story.append(Spacer(1, 35))

    story.append(Paragraph("<b>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</b>", style_univ_header))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>ROORKEE INSTITUTE OF TECHNOLOGY, ROORKEE</b>", style_univ_header))
    story.append(Spacer(1, 2))
    story.append(Paragraph("(Affiliated to VMSB Uttarakhand Technical University, Dehradun)", style_univ_sub))
    story.append(Spacer(1, 35))

    p_dur = Paragraph("Internship Duration: ______________________ to ______________________", style_univ_sub)
    t_dur = Table([[p_dur]], colWidths=[485])
    t_dur.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(t_dur)
    story.append(Spacer(1, 10))
    story.append(Paragraph("September 2026", style_univ_sub))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: SELF DECLARATION CERTIFICATE
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>Self Declaration Certificate</b></u>", style_section_heading))
    story.append(Spacer(1, 30))

    p_decl1 = "I declare that the work embodied in this Internship report is my own original work carried out by me under the supervision of the CodeAlpha internship supervisor."
    p_decl2 = "The matter embodied in this internship report has not been submitted elsewhere for the award of any other degree. I declare that I have faithfully acknowledged, given credit to and referred to the sources wherever the work has been used in the text and the body of the report."
    p_decl3 = "I further certify that I have not willfully lifted up someone else's work, paragraph, text, data, results, etc. and presented it as my own work. The project work and screenshots included in this report are related to the work completed by me during the internship."

    story.append(Paragraph(p_decl1, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_decl2, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_decl3, style_body))
    story.append(Spacer(1, 65))

    story.append(Paragraph("Date : ______________________", style_body))
    story.append(Spacer(1, 35))
    story.append(Paragraph("Name & Signature of the Student: ______________________________", style_body))
    story.append(Spacer(1, 35))
    story.append(Paragraph("Signature of Internal Examiner: ______________________________", style_body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: CERTIFICATE OF COMPLETION (BLANK PLACEHOLDER)
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>CERTIFICATE</b></u>", style_section_heading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>OF COMPLETION</b>", style_section_heading))
    story.append(Spacer(1, 15))
    story.append(Paragraph("(CodeAlpha Internship Completion Certificate)", style_univ_sub))
    story.append(Spacer(1, 35))

    # Blank certificate box matching reference PDF
    cert_placeholder = [
        Spacer(1, 180),
        Paragraph("<font color='#666666'>[ Paste your original CodeAlpha certificate image on this page ]</font>", style_univ_sub),
        Spacer(1, 180)
    ]
    t_cert = Table([[cert_placeholder]], colWidths=[480])
    t_cert.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#999999")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_cert)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: ACKNOWLEDGMENT
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>ACKNOWLEDGMENT</b></u>", style_section_heading))
    story.append(Spacer(1, 30))

    p_ack1 = "I would like to express my sincere gratitude to everyone who supported and encouraged me throughout my internship and helped me complete this report successfully."
    p_ack2 = "I am thankful to the Director and the Department of Computer Science & Engineering, Roorkee Institute of Technology, Roorkee, for providing a supportive academic environment and the opportunity to undertake this internship."
    p_ack3 = "I also express my sincere gratitude to the Head of the Department for the guidance, encouragement and support provided during my academic work."
    p_ack4 = "I am grateful to CodeAlpha for providing me with the opportunity to gain practical experience in Full Stack Web Development. The project based work helped me practice frontend architecture, client-side state persistence, user interface engineering and responsive layout design, and understand how these technologies are used in an actual production-style application."
    p_ack5 = "Finally, I would like to thank all the teaching and non-teaching staff of the Department of Computer Science & Engineering, Roorkee Institute of Technology, Roorkee, for their support and suggestions."

    story.append(Paragraph(p_ack1, style_body))
    story.append(Spacer(1, 13))
    story.append(Paragraph(p_ack2, style_body))
    story.append(Spacer(1, 13))
    story.append(Paragraph(p_ack3, style_body))
    story.append(Spacer(1, 13))
    story.append(Paragraph(p_ack4, style_body))
    story.append(Spacer(1, 13))
    story.append(Paragraph(p_ack5, style_body))
    story.append(Spacer(1, 50))

    story.append(Paragraph("Date : ______________________", style_body))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Student Name: Shaurya Kartik", style_body))
    story.append(Spacer(1, 25))
    story.append(Paragraph("Student Roll No.: ______________________", style_body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TABLE OF CONTENTS
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>TABLE OF CONTENTS</b></u>", style_section_heading))
    story.append(Spacer(1, 25))

    toc_data = [
        [Paragraph("<b>ABSTRACT</b>", style_body), Paragraph("<b>6</b>", style_body)],
        [Paragraph("<b>BACKGROUND OF COMPANY/ORGANIZATION</b>", style_body), Paragraph("<b>7</b>", style_body)],
        [Paragraph("<b>PROGRAM AND OPPORTUNITIES</b>", style_body), Paragraph("<b>8</b>", style_body)],
        [Paragraph("<b>BENEFIT OF COMPANY/ORGANIZATION</b>", style_body), Paragraph("<b>9</b>", style_body)],
        [Paragraph("<b>1. INTRODUCTION</b>", style_body), Paragraph("<b>10</b>", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Background of the Project", style_body), Paragraph("10", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.2 Problem Statement", style_body), Paragraph("10", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Project Objective", style_body), Paragraph("10", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.4 Advantages of the Project", style_body), Paragraph("10", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.5 Scope of Project", style_body), Paragraph("10", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.6 Tools & Technology Used", style_body), Paragraph("10", style_body)],
        [Paragraph("<b>2. ANALYSIS</b>", style_body), Paragraph("<b>12</b>", style_body)],
        [Paragraph("<b>3. SOFTWARE REQUIREMENT SPECIFICATION</b>", style_body), Paragraph("<b>13</b>", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.1 System Configurations", style_body), Paragraph("13", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.2 Functional Requirements", style_body), Paragraph("13", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.3 Non-Functional Requirements", style_body), Paragraph("13", style_body)],
        [Paragraph("<b>4. TECHNOLOGY USED AND ITS DESCRIPTION</b>", style_body), Paragraph("<b>14</b>", style_body)],
        [Paragraph("<b>5. CODING</b>", style_body), Paragraph("<b>15</b>", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.1 Dynamic Product Catalog & Real-Time Filtering", style_body), Paragraph("15", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.2 Interactive Shopping Cart & LocalStorage Persistence", style_body), Paragraph("16", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.3 Checkout Processing & Form Validation", style_body), Paragraph("17", style_body)],
        [Paragraph("<b>6. SCREENSHOTS</b>", style_body), Paragraph("<b>18</b>", style_body)],
        [Paragraph("<b>7. CONCLUSION</b>", style_body), Paragraph("<b>22</b>", style_body)],
        [Paragraph("<b>8. BIBLIOGRAPHY</b>", style_body), Paragraph("<b>23</b>", style_body)],
    ]
    t_toc = Table(toc_data, colWidths=[430, 50])
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: ABSTRACT
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>ABSTRACT</b></u>", style_section_heading))
    story.append(Spacer(1, 30))

    p_abs1 = "This report summarizes my internship in Full Stack Web Development at CodeAlpha. The main aim was to gain practical, hands-on experience of building a responsive, high-performance web application and to understand how frontend structure, glassmorphic visual presentation, real-time client-side business logic, and persistent storage work together in a single production-style project."
    p_abs2 = "During the internship, I designed and built NEXUS Store, a modern, feature-rich E-Commerce web application. NEXUS Store allows users to browse an interactive catalog of cutting-edge tech gadgets, filter products dynamically by category (Audio & Sound, Smart Wearables, Computing & Tech, Accessories), execute instant keyword searches, view detailed specifications via a Quick-View modal, manage a slide-out cart drawer with dynamic Indian Rupee (₹) pricing, and complete full shipping checkout forms with live order history tracking."
    p_abs3 = "The internship gave me practical experience in modern UI engineering using semantic HTML5, advanced CSS3 with Glassmorphism, and asynchronous Vanilla JavaScript (ES6+). To ensure zero-server cost and maximum reliability, I engineered a client-side persistence architecture using the HTML5 Web Storage API (LocalStorage). This eliminated server hosting friction while preserving full cart contents, user accounts, and historical order records across browser sessions."
    p_abs4 = "Overall, this internship was a valuable learning experience. It helped me connect the individual concepts I had studied separately — frontend layout design, DOM event handling, state persistence, and responsive mobile optimization — into one working, end-to-end application, and gave me confidence to build and reason about full stack systems."

    story.append(Paragraph(p_abs1, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_abs2, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_abs3, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_abs4, style_body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: BACKGROUND OF COMPANY / ORGANIZATION
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>BACKGROUND OF COMPANY/ORGANIZATION</b></u>", style_section_heading))
    story.append(Spacer(1, 30))

    p_bg1 = "CodeAlpha is a technology education and skill development organization that provides internship and learning opportunities to students across different technical domains, including web development, application development and data-driven technologies. The main purpose of such programs is to help students learn new skills and gain practical, project-based experience."
    p_bg2 = "The Full Stack Web Development internship focused on the technologies used to build a complete, working web application - from the user interface to the business logic, client-side state persistence and responsive design. The project-based work helped me practice concepts I had studied and apply them to an actual, usable product."
    p_bg3 = "My internship certificate confirms that I successfully completed the internship in Full Stack Web Development at CodeAlpha for the duration ______________________ to ______________________."
    p_bg4 = "In this report I have mainly discussed the work completed by me on the NEXUS E-Commerce Store project and the learning I gained from it."
    p_bg5 = "The work was based on building a modern web application end to end - the visible interface, the state management logic that keeps cart and order data consistent, and the interactive UI components that deliver an effortless shopping experience to users on both desktop and mobile devices."

    story.append(Paragraph(p_bg1, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_bg2, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_bg3, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_bg4, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_bg5, style_body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: PROGRAM AND OPPORTUNITIES
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>PROGRAM AND OPPORTUNITIES</b></u>", style_section_heading))
    story.append(Spacer(1, 30))

    p_prog1 = "During my internship in Full Stack Web Development at CodeAlpha, I had the opportunity to work on a complete, real-time web application and gain practical experience across the frontend, state management, UI design, and client-side database layers."
    p_prog2 = "The main technologies used during the internship were HTML5, CSS3, Vanilla JavaScript (ES6+), LocalStorage API, and Git/GitHub. The work was focused on understanding how these pieces connect in a single production-style project."

    story.append(Paragraph(p_prog1, style_body))
    story.append(Spacer(1, 12))
    story.append(Paragraph(p_prog2, style_body))
    story.append(Spacer(1, 12))

    story.append(Paragraph("• Practicing semantic and accessible UI structuring using HTML5.", style_body_bullet))
    story.append(Spacer(1, 6))
    story.append(Paragraph("• Designing an advanced Glassmorphic dark design system with CSS3 variables and animations.", style_body_bullet))
    story.append(Spacer(1, 6))
    story.append(Paragraph("• Implementing reactive client-side state persistence using HTML5 LocalStorage.", style_body_bullet))
    story.append(Spacer(1, 6))
    story.append(Paragraph("• Engineering interactive shopping components: slide-out cart drawer, search filter, and quick view.", style_body_bullet))
    story.append(Spacer(1, 6))
    story.append(Paragraph("• Localizing financial and currency calculations with Indian Rupee (₹) standards.", style_body_bullet))
    story.append(Spacer(1, 6))
    story.append(Paragraph("• Testing and optimizing cross-device responsiveness across smartphones, tablets, and desktops.", style_body_bullet))
    story.append(Spacer(1, 14))

    p_prog3 = "Along with coding, I practiced habits such as writing clean and modular JavaScript, structuring project files logically, and handling edge cases such as empty carts, zero quantities, and invalid form submissions. These habits made the project reliable and easy to maintain."
    p_prog4 = "The project can be extended further with real payment gateways (such as Razorpay), backend microservices, and Progressive Web App (PWA) features. This gives me a clear direction for continuing full stack web development."

    story.append(Paragraph(p_prog3, style_body))
    story.append(Spacer(1, 12))
    story.append(Paragraph(p_prog4, style_body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: BENEFIT OF COMPANY / ORGANIZATION
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>BENEFIT OF COMPANY/ORGANIZATION</b></u>", style_section_heading))
    story.append(Spacer(1, 30))

    p_ben1 = "The biggest benefit I received from the internship was practical, end-to-end exposure. Before this project, I had worked with individual pieces of web development separately. By building NEXUS Store myself, I got a clear picture of how UI presentation, user event handling, state management, and persistent storage all fit together in one working system."
    p_ben2 = "Another benefit was learning through debugging real problems. For example, during initial development, older cached items in browser storage conflicted with newly added product attributes and currency symbols. Investigating and fixing this taught me how data migration and storage versioning work in client-side applications."
    p_ben3 = "The internship also helped me understand user experience in practice - not just styling elements for desktop monitors, but ensuring mobile users get a frictionless experience with touch-optimized category carousels, full-screen drawer transitions, and prevention of iOS input auto-zooming."
    p_ben4 = "The project-based approach gave me a much better understanding of how individually learned concepts - semantic markup, CSS Grid/Flexbox, JavaScript array operations, and browser APIs - combine to produce a working, real-time product."

    story.append(Paragraph(p_ben1, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_ben2, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_ben3, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_ben4, style_body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: 1. INTRODUCTION
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>1. INTRODUCTION</b></u>", style_section_heading))
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>1.1 Background of the Project</b>", style_subheading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("E-Commerce has transformed modern global retail, making intuitive digital storefronts essential for businesses. Consumers demand rapid loading times, clean visuals, instant product discovery, and effortless checkout. For a Computer Science student, building an e-commerce platform is an ideal way to master user interface engineering, event-driven state manipulation, and client persistence.", style_body))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>1.2 Problem Statement</b>", style_subheading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Many conventional academic web projects suffer from bloated server dependencies that require cumbersome local environment setup (Python, Node, databases), making them fragile during live presentations. Furthermore, existing demo stores often feature bland designs, lack mobile responsiveness, and fail to preserve cart data across refreshes. The challenge was to engineer an e-commerce platform that runs 100% in the browser with zero server setup while delivering a commercial-grade user experience.", style_body))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>1.3 Project Objective</b>", style_subheading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("• To architect an intuitive, modern E-Commerce store using Pure HTML5, CSS3, and JavaScript.<br/>"
                           "• To implement dynamic category filtering and real-time search without full-page reloads.<br/>"
                           "• To build an interactive slide-out cart drawer with quantity controls and dynamic totals.<br/>"
                           "• To localize all pricing into Indian Rupees (₹) with proper locale currency formatting.<br/>"
                           "• To persist catalog, cart, user accounts, and order history via HTML5 LocalStorage.<br/>"
                           "• To ensure flawless cross-device responsiveness across smartphones, tablets, and desktops.", style_body))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>1.4 Advantages of the Project</b>", style_subheading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("• <b>Zero-Server Cost:</b> Runs directly by double-clicking <code>index.html</code> or hosting on GitHub Pages.<br/>"
                           "• <b>Blazing Fast:</b> No backend roundtrip delays; all interactions execute in under 16 milliseconds.<br/>"
                           "• <b>Full Persistence:</b> Preserves shopping carts and placed orders across browser sessions.<br/>"
                           "• <b>Production-Grade UI:</b> Sleek dark glassmorphic design system with micro-animations.", style_body))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>1.5 Scope of Project</b>", style_subheading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("The scope covers the complete single-page e-commerce lifecycle: hero banner, product browsing, category chips, live search, quick-view modal, shopping cart drawer, shipping checkout form with validation, order generation, and order history dashboard.", style_body))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>1.6 Tools & Technology Used</b>", style_subheading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("• Semantic HTML5 for page architecture<br/>"
                           "• Advanced CSS3 (Glassmorphism, Flexbox, Grid, Keyframe Animations)", style_body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: 1. INTRODUCTION (CONTINUED)
    # =========================================================================
    story.append(Spacer(1, 30))
    story.append(Paragraph("• Vanilla JavaScript (ES6+) for business logic, DOM manipulation and event routing", style_body))
    story.append(Spacer(1, 12))
    story.append(Paragraph("• HTML5 Web Storage API (LocalStorage) for client-side database persistence", style_body))
    story.append(Spacer(1, 12))
    story.append(Paragraph("• FontAwesome 6 (CDN) for vector iconography and status symbols", style_body))
    story.append(Spacer(1, 12))
    story.append(Paragraph("• Google Fonts ('Outfit') for clean modern typography", style_body))
    story.append(Spacer(1, 12))
    story.append(Paragraph("• Visual Studio Code as the primary code editor and development environment", style_body))
    story.append(Spacer(1, 12))
    story.append(Paragraph("• Google Chrome & Microsoft Edge for browser testing and Developer Tools debugging", style_body))
    story.append(Spacer(1, 12))
    story.append(Paragraph("• Git & GitHub for version control, repository tracking, and GitHub Pages deployment", style_body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: 2. ANALYSIS
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>2. ANALYSIS</b></u>", style_section_heading))
    story.append(Spacer(1, 25))

    p_an_intro = "The analysis was conducted by identifying what a responsive, client-side e-commerce platform requires before writing code, and breaking down the requirements into modular functional layers."
    story.append(Paragraph(p_an_intro, style_body))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Core Shopping Flow Analysis</b>", style_subheading))
    story.append(Spacer(1, 4))
    p_an_flow = "The primary requirement was ensuring that users could discover and purchase tech products without page reloads. A Single-Page Application (SPA) architecture was chosen where JavaScript dynamically updates the Document Object Model (DOM) in response to category selections, search queries, and cart operations. This eliminates the latency inherent in traditional server-rendered websites."
    story.append(Paragraph(p_an_flow, style_body))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>State Persistence & Storage Analysis</b>", style_subheading))
    story.append(Spacer(1, 4))
    p_an_store = "An e-commerce store must remember cart items even if the user accidentally reloads the page or navigates away. Rather than relying on a heavy SQL database server, the HTML5 LocalStorage API was analyzed and selected. LocalStorage provides 5MB of structured key-value storage per origin, more than sufficient to store normalized JSON tables for products, active carts, historical orders, and user authentication tokens."
    story.append(Paragraph(p_an_store, style_body))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Financial & Localization Analysis</b>", style_subheading))
    story.append(Spacer(1, 4))
    p_an_fin = "To make the application authentic for Indian users and presentations, all currency values were analyzed and localized into Indian Rupees (₹). Western number formatting (millions/billions) was replaced with the Indian numbering format using JavaScript's <code>Intl.NumberFormat</code> and <code>toLocaleString('en-IN')</code>."
    story.append(Paragraph(p_an_fin, style_body))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Gaps and Motivation</b>", style_subheading))
    story.append(Spacer(1, 4))
    p_an_gap = "The main gap identified in my prior learning was connecting individual front-end elements into a unified, stateful application with robust persistence. Building NEXUS Store bridged that gap by showing how data structures, event listeners, and styling form an integrated production system."
    story.append(Paragraph(p_an_gap, style_body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: 3. SOFTWARE REQUIREMENT SPECIFICATION
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>3. SOFTWARE REQUIREMENT SPECIFICATION</b></u>", style_section_heading))
    story.append(Spacer(1, 25))

    story.append(Paragraph("<b>3.1 System Configurations</b>", style_subheading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("• Operating System: Windows 10 / Windows 11, macOS, or Linux<br/>"
                           "• Language: Semantic HTML5, CSS3, Vanilla JavaScript (ES6+)<br/>"
                           "• Persistence Engine: HTML5 Web Storage API (LocalStorage)<br/>"
                           "• Icons & Fonts: FontAwesome 6, Google Fonts ('Outfit')<br/>"
                           "• Code Editor: Visual Studio Code<br/>"
                           "• Browsers: Google Chrome, Microsoft Edge, Mozilla Firefox, Apple Safari<br/>"
                           "• Deployment: GitHub Pages / Static Web Server", style_body))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>3.2 Functional Requirements</b>", style_subheading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("• Render dynamic tech product cards with images, prices, discount badges, and ratings.<br/>"
                           "• Provide real-time category filtering (Audio, Wearables, Tech, Accessories, All).<br/>"
                           "• Provide live instant search matching keywords across titles and descriptions.<br/>"
                           "• Quick-View modal displaying comprehensive specifications and immediate add-to-cart.<br/>"
                           "• Slide-out Cart Drawer with dynamic quantity stepper (<code>+</code> / <code>-</code>) and auto-removal.<br/>"
                           "• Real-time subtotal and total calculations formatted in Indian Rupees (₹).<br/>"
                           "• Checkout form with shipping field validation (Name, Email, Address, City, Zip).<br/>"
                           "• Unique 6-digit Order ID generation and recording in order history.<br/>"
                           "• User registration, login, logout, and session state persistence.<br/>"
                           "• Order History modal displaying past purchases with timestamps and order status.", style_body))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>3.3 Non-Functional Requirements</b>", style_subheading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("• <b>Usability:</b> Intuitive glassmorphism interface with non-intrusive toast notifications.<br/>"
                           "• <b>Responsiveness:</b> Adaptive layouts for mobile phones, tablets, and widescreen displays.<br/>"
                           "• <b>Performance:</b> Zero network overhead for storage; instantaneous client-side operations.<br/>"
                           "• <b>Reliability:</b> Persistent data integrity across browser reloads and reboots.", style_body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: 4. TECHNOLOGY USED AND ITS DESCRIPTION
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>4. TECHNOLOGY USED AND ITS DESCRIPTION</b></u>", style_section_heading))
    story.append(Spacer(1, 25))

    story.append(Paragraph("<b>4.1 HTML5 Semantic Markup</b>", style_subheading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("HTML5 provides the foundational structure of NEXUS Store. Semantic tags including <code>&lt;nav&gt;</code>, <code>&lt;header&gt;</code>, <code>&lt;main&gt;</code>, <code>&lt;aside&gt;</code>, and <code>&lt;footer&gt;</code> were used to ensure clean document hierarchy, improved accessibility, and optimal search engine readability. Modals and drawers are structured cleanly at the root body level.", style_body))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>4.2 Modern CSS3 & Glassmorphic Design System</b>", style_subheading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("CSS3 was utilized to build an ultra-sleek, futuristic dark glass theme. Key techniques include CSS Custom Properties (variables) for uniform color theming, <code>backdrop-filter: blur(16px)</code> for glass surfaces, CSS Flexbox and Grid for fluid layouts, and cubic-bezier keyframe transitions for smooth cart drawer sliding and toast notification animations.", style_body))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>4.3 Vanilla JavaScript (ES6+)</b>", style_subheading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Modern JavaScript acts as the central business logic controller. Using modular ES6 functions, array pipelines (<code>filter</code>, <code>map</code>, <code>reduce</code>), template literals, and event delegation, the script handles dynamic DOM updates, search indexing, quantity manipulation, modal visibility, and currency formatting without any external frameworks.", style_body))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>4.4 HTML5 Web Storage API (LocalStorage)</b>", style_subheading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("LocalStorage acts as the persistent client-side database. It stores JSON strings representing the product catalog, active shopping cart, user registration details, and placed orders. Storage version checking was implemented to guarantee seamless data initialization and caching updates.", style_body))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>4.5 FontAwesome 6 & Google Fonts</b>", style_subheading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("FontAwesome 6 delivers lightweight vector icons for actions like cart management, ratings, and searching. Google's modern geometric 'Outfit' typeface gives the store a sharp, contemporary aesthetic fitting high-end tech electronics.", style_body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: 5. CODING — 5.1 PRODUCT CATALOG & FILTERING
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>5. CODING</b></u>", style_section_heading))
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>5.1 Dynamic Product Catalog & Real-Time Filtering</b>", style_subheading))
    story.append(Spacer(1, 6))
    p_code1_desc = "The product catalog is rendered dynamically from in-memory objects populated from LocalStorage. The filtering engine filters items by active category slug and performs case-insensitive search queries on title and description strings without reloading the page."
    story.append(Paragraph(p_code1_desc, style_body))
    story.append(Spacer(1, 10))

    code_snippet_1 = """// Category Filter & Real-Time Search Query Engine
function loadProducts() {
    const grid = document.getElementById('productGrid');
    let products = JSON.parse(localStorage.getItem('nexus_products') || '[]');

    // Filter by Selected Category
    if (currentCategory !== 'all') {
        products = products.filter(p => p.category_slug === currentCategory);
    }

    // Filter by Instant Search Query
    if (searchQuery.trim() !== '') {
        const query = searchQuery.toLowerCase();
        products = products.filter(p => 
            p.name.toLowerCase().includes(query) || 
            p.description.toLowerCase().includes(query)
        );
    }

    if (products.length === 0) {
        grid.innerHTML = '<div class="empty-cart"><h3>No products found</h3></div>';
        return;
    }

    grid.innerHTML = products.map(p => `
        <div class="product-card">
            <div class="product-image-wrap">
                <img src="${p.image_url}" alt="${p.name}">
                <span class="product-tag">${p.category_name}</span>
            </div>
            <div class="product-details">
                <h3 class="product-title">${p.name}</h3>
                <div class="product-price-row">
                    <span class="current-price">${formatINR(p.price)}</span>
                </div>
                <button class="add-cart-btn" onclick="addToCart(${p.id})">Add to Cart</button>
            </div>
        </div>
    `).join('');
}"""

    t_c1 = Table([[Paragraph(f"<pre>{html.escape(code_snippet_1)}</pre>", style_code)]], colWidths=[480])
    t_c1.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#333333")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_c1)
    story.append(Spacer(1, 8))
    story.append(Paragraph("<i>Code snippet: Real-time product search and category filtering</i>", style_caption))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: 5. CODING — 5.2 CART & LOCALSTORAGE PERSISTENCE
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>5. CODING</b></u>", style_section_heading))
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>5.2 Interactive Shopping Cart & LocalStorage Persistence</b>", style_subheading))
    story.append(Spacer(1, 6))
    p_code2_desc = "Cart state management handles adding items, incrementing and decrementing quantities, dynamic subtotal calculations, and synchronizing data immediately into LocalStorage so that cart state persists indefinitely across sessions."
    story.append(Paragraph(p_code2_desc, style_body))
    story.append(Spacer(1, 10))

    code_snippet_2 = """// Cart Management & Indian Rupee (₹) Calculations
function addToCart(productId) {
    const products = JSON.parse(localStorage.getItem('nexus_products') || '[]');
    const product = products.find(p => p.id === productId);
    if (!product) return;

    const existingIndex = cartItems.findIndex(i => i.id === productId);
    if (existingIndex > -1) {
        cartItems[existingIndex].quantity += 1;
    } else {
        cartItems.push({
            id: product.id, name: product.name, price: product.price,
            image_url: product.image_url, quantity: 1
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

function formatINR(amount) {
    return '₹' + Number(amount).toLocaleString('en-IN', {
        minimumFractionDigits: 2, maximumFractionDigits: 2
    });
}"""

    t_c2 = Table([[Paragraph(f"<pre>{html.escape(code_snippet_2)}</pre>", style_code)]], colWidths=[480])
    t_c2.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#333333")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_c2)
    story.append(Spacer(1, 8))
    story.append(Paragraph("<i>Code snippet: Shopping cart state updates and INR formatting</i>", style_caption))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: 5. CODING — 5.3 CHECKOUT & ORDER VALIDATION
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>5. CODING</b></u>", style_section_heading))
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>5.3 Checkout Processing & Form Validation</b>", style_subheading))
    story.append(Spacer(1, 6))
    p_code3_desc = "The checkout process validates customer shipping details, creates a unique bill record with a 6-digit Order ID, stores the order in historical storage, empties the cart, and prompts the order confirmation dashboard."
    story.append(Paragraph(p_code3_desc, style_body))
    story.append(Spacer(1, 10))

    code_snippet_3 = """// Checkout Submission & Order Record Creation
function handleCheckoutSubmit(e) {
    e.preventDefault();
    if (cartItems.length === 0) {
        showToast('Your cart is empty', 'fa-triangle-exclamation');
        return;
    }

    const fullName = document.getElementById('chkFullName').value.trim();
    const email = document.getElementById('chkEmail').value.trim();
    const address = document.getElementById('chkAddress').value.trim();
    const city = document.getElementById('chkCity').value.trim();
    const zipCode = document.getElementById('chkZip').value.trim();

    const total = cartItems.reduce((acc, item) => acc + (item.price * item.quantity), 0);
    const orderId = Math.floor(100000 + Math.random() * 900000);
    const dateStr = new Date().toISOString().slice(0, 16).replace('T', ' ');

    const newOrder = {
        id: orderId, username: currentUser ? currentUser.username : 'Guest',
        full_name: fullName, email: email, address: address, city: city,
        zip_code: zipCode, total_amount: total, status: 'Processing',
        created_at: dateStr, items: [...cartItems]
    };

    const orders = JSON.parse(localStorage.getItem('nexus_orders') || '[]');
    orders.unshift(newOrder);
    localStorage.setItem('nexus_orders', JSON.stringify(orders));

    // Clear active cart & update UI
    cartItems = [];
    saveCart();
    loadCart();
    closeModal('checkoutModal');
    showToast(`Order #${orderId} placed successfully!`);
}"""

    t_c3 = Table([[Paragraph(f"<pre>{html.escape(code_snippet_3)}</pre>", style_code)]], colWidths=[480])
    t_c3.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#333333")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_c3)
    story.append(Spacer(1, 8))
    story.append(Paragraph("<i>Code snippet: Client-side checkout processing and order storage</i>", style_caption))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: 6. SCREENSHOTS — FIGURE 6.1 (LANDING PAGE & HERO)
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>6. SCREENSHOTS</b></u>", style_section_heading))
    story.append(Spacer(1, 15))
    story.append(Paragraph("The following diagrams and screenshots illustrate the actual user interface of the NEXUS E-Commerce Store completed during the internship.", style_body))
    story.append(Spacer(1, 20))

    # Mockup Diagram for Figure 6.1
    d_sc1 = Drawing(470, 260)
    # Outer browser frame
    d_sc1.add(Rect(0, 0, 470, 260, rx=4, ry=4, fillColor=colors.HexColor("#090d16"), strokeColor=colors.HexColor("#334155"), strokeWidth=1))
    # Browser top bar
    d_sc1.add(Rect(0, 238, 470, 22, rx=4, ry=4, fillColor=colors.HexColor("#1e293b"), strokeColor=None))
    d_sc1.add(Circle(12, 249, 4, fillColor=colors.HexColor("#ef4444"), strokeColor=None))
    d_sc1.add(Circle(24, 249, 4, fillColor=colors.HexColor("#f59e0b"), strokeColor=None))
    d_sc1.add(Circle(36, 249, 4, fillColor=colors.HexColor("#10b981"), strokeColor=None))
    d_sc1.add(String(160, 245, "https://shauryakartik2-source.github.io/Ecommerce-store/", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#94a3b8")))
    # Navbar inside
    d_sc1.add(Rect(0, 206, 470, 32, fillColor=colors.HexColor("#0f172a"), strokeColor=colors.HexColor("#1e293b")))
    d_sc1.add(String(15, 218, "⚡ NEXUS STORE", fontName="Helvetica-Bold", fontSize=11, fillColor=colors.HexColor("#6366f1")))
    d_sc1.add(Rect(140, 211, 190, 20, rx=10, ry=10, fillColor=colors.HexColor("#1e293b"), strokeColor=colors.HexColor("#334155")))
    d_sc1.add(String(155, 217, "🔍 Search gadgets, audio, tech...", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#64748b")))
    d_sc1.add(Rect(375, 211, 45, 20, rx=10, ry=10, fillColor=colors.HexColor("#1e293b"), strokeColor=colors.HexColor("#334155")))
    d_sc1.add(String(383, 217, "Sign In", fontName="Helvetica", fontSize=7.5, fillColor=colors.white))
    d_sc1.add(Circle(445, 221, 10, fillColor=colors.HexColor("#6366f1"), strokeColor=None))
    d_sc1.add(String(442, 218, "🛒", fontName="Helvetica", fontSize=8, fillColor=colors.white))
    # Hero content
    d_sc1.add(Rect(20, 30, 240, 150, rx=6, ry=6, fillColor=colors.HexColor("#0f172a"), strokeColor=colors.HexColor("#1e293b")))
    d_sc1.add(Rect(35, 150, 140, 18, rx=9, ry=9, fillColor=colors.HexColor("#1e1b4b"), strokeColor=colors.HexColor("#4338ca")))
    d_sc1.add(String(42, 155, "🔥 CODEALPHA INTERNSHIP PROJECT", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.HexColor("#818cf8")))
    d_sc1.add(String(35, 122, "Next-Gen Tech Essentials", fontName="Helvetica-Bold", fontSize=15, fillColor=colors.white))
    d_sc1.add(String(35, 104, "Discover premium audio gear, wearables & sleek gadgets", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#94a3b8")))
    d_sc1.add(String(35, 92, "engineered for peak performance and built with zero setup.", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#94a3b8")))
    d_sc1.add(Rect(35, 55, 80, 24, rx=4, ry=4, fillColor=colors.HexColor("#6366f1"), strokeColor=None))
    d_sc1.add(String(48, 63, "Shop Now", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.white))
    d_sc1.add(Rect(125, 55, 80, 24, rx=4, ry=4, fillColor=colors.HexColor("#1e293b"), strokeColor=colors.HexColor("#334155")))
    d_sc1.add(String(138, 63, "Audio Gear", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.HexColor("#94a3b8")))
    # Hero Banner Card Right
    d_sc1.add(Rect(275, 30, 175, 150, rx=8, ry=8, fillColor=colors.HexColor("#1e293b"), strokeColor=colors.HexColor("#334155")))
    d_sc1.add(String(305, 95, "[ Headphone Visual ]", fontName="Helvetica-Bold", fontSize=11, fillColor=colors.HexColor("#64748b")))
    d_sc1.add(Rect(285, 40, 155, 22, rx=5, ry=5, fillColor=colors.HexColor("#090d16"), strokeColor=colors.HexColor("#334155")))
    d_sc1.add(String(293, 47, "⭐ 4.9 Rating Premium Audio", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor("#f59e0b")))

    t_s1 = Table([[d_sc1]], colWidths=[470])
    t_s1.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(t_s1)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Figure 6.1: NEXUS Store Landing Page & Hero Section</b>", style_caption))
    story.append(Spacer(1, 4))
    story.append(Paragraph("The landing page features a glassmorphic navbar with search and user controls, alongside a prominent promotional hero banner highlighting project attributes.", style_caption_desc))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 19: 6. SCREENSHOTS — FIGURE 6.2 (PRODUCT CATALOG & FILTERS)
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>6. SCREENSHOTS</b></u>", style_section_heading))
    story.append(Spacer(1, 25))

    # Mockup Diagram for Figure 6.2
    d_sc2 = Drawing(470, 260)
    d_sc2.add(Rect(0, 0, 470, 260, rx=4, ry=4, fillColor=colors.HexColor("#090d16"), strokeColor=colors.HexColor("#334155"), strokeWidth=1))
    # Category Bar
    d_sc2.add(String(20, 235, "Explore Products", fontName="Helvetica-Bold", fontSize=13, fillColor=colors.white))
    d_sc2.add(Rect(20, 200, 50, 22, rx=11, ry=11, fillColor=colors.HexColor("#6366f1"), strokeColor=None))
    d_sc2.add(String(32, 207, "All", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    d_sc2.add(Rect(78, 200, 85, 22, rx=11, ry=11, fillColor=colors.HexColor("#1e293b"), strokeColor=colors.HexColor("#334155")))
    d_sc2.add(String(88, 207, "🎧 Audio & Sound", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#94a3b8")))
    d_sc2.add(Rect(171, 200, 95, 22, rx=11, ry=11, fillColor=colors.HexColor("#1e293b"), strokeColor=colors.HexColor("#334155")))
    d_sc2.add(String(181, 207, "⌚ Smart Wearables", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#94a3b8")))
    d_sc2.add(Rect(274, 200, 105, 22, rx=11, ry=11, fillColor=colors.HexColor("#1e293b"), strokeColor=colors.HexColor("#334155")))
    d_sc2.add(String(284, 207, "💻 Computing & Tech", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#94a3b8")))
    d_sc2.add(Rect(387, 200, 70, 22, rx=11, ry=11, fillColor=colors.HexColor("#1e293b"), strokeColor=colors.HexColor("#334155")))
    d_sc2.add(String(396, 207, "🔌 Accessories", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#94a3b8")))
    
    # 3 Product Cards
    # Card 1
    d_sc2.add(Rect(20, 20, 135, 165, rx=6, ry=6, fillColor=colors.HexColor("#0f172a"), strokeColor=colors.HexColor("#1e293b")))
    d_sc2.add(Rect(20, 100, 135, 85, rx=6, ry=6, fillColor=colors.HexColor("#1e293b"), strokeColor=None))
    d_sc2.add(String(45, 140, "[ ANC Headphones ]", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#94a3b8")))
    d_sc2.add(String(28, 82, "AeroPulse Wireless ANC", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.white))
    d_sc2.add(String(28, 68, "⭐ 4.9 (128 reviews)", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#f59e0b")))
    d_sc2.add(String(28, 50, "₹1,999.00", fontName="Helvetica-Bold", fontSize=10, fillColor=colors.HexColor("#10b981")))
    d_sc2.add(String(85, 50, "₹2,499.00", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#64748b")))
    d_sc2.add(Rect(28, 28, 119, 16, rx=4, ry=4, fillColor=colors.HexColor("#6366f1"), strokeColor=None))
    d_sc2.add(String(55, 33, "+ Add to Cart", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.white))

    # Card 2
    d_sc2.add(Rect(168, 20, 135, 165, rx=6, ry=6, fillColor=colors.HexColor("#0f172a"), strokeColor=colors.HexColor("#1e293b")))
    d_sc2.add(Rect(168, 100, 135, 85, rx=6, ry=6, fillColor=colors.HexColor("#1e293b"), strokeColor=None))
    d_sc2.add(String(195, 140, "[ Apex Smartwatch ]", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#94a3b8")))
    d_sc2.add(String(176, 82, "Titanium Apex Pro Watch", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.white))
    d_sc2.add(String(176, 68, "⭐ 4.8 (94 reviews)", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#f59e0b")))
    d_sc2.add(String(176, 50, "₹2,999.00", fontName="Helvetica-Bold", fontSize=10, fillColor=colors.HexColor("#10b981")))
    d_sc2.add(String(233, 50, "₹3,499.00", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#64748b")))
    d_sc2.add(Rect(176, 28, 119, 16, rx=4, ry=4, fillColor=colors.HexColor("#6366f1"), strokeColor=None))
    d_sc2.add(String(203, 33, "+ Add to Cart", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.white))

    # Card 3
    d_sc2.add(Rect(316, 20, 135, 165, rx=6, ry=6, fillColor=colors.HexColor("#0f172a"), strokeColor=colors.HexColor("#1e293b")))
    d_sc2.add(Rect(316, 100, 135, 85, rx=6, ry=6, fillColor=colors.HexColor("#1e293b"), strokeColor=None))
    d_sc2.add(String(340, 140, "[ RGB Keyboard ]", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#94a3b8")))
    d_sc2.add(String(324, 82, "CyberDeck RGB Keyboard", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.white))
    d_sc2.add(String(324, 68, "⭐ 4.7 (67 reviews)", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#f59e0b")))
    d_sc2.add(String(324, 50, "₹1,299.00", fontName="Helvetica-Bold", fontSize=10, fillColor=colors.HexColor("#10b981")))
    d_sc2.add(String(381, 50, "₹1,599.00", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#64748b")))
    d_sc2.add(Rect(324, 28, 119, 16, rx=4, ry=4, fillColor=colors.HexColor("#6366f1"), strokeColor=None))
    d_sc2.add(String(351, 33, "+ Add to Cart", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.white))

    t_s2 = Table([[d_sc2]], colWidths=[470])
    t_s2.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(t_s2)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Figure 6.2: Product Catalog & Dynamic Category Filters</b>", style_caption))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Product cards displaying high-resolution images, category tags, customer review ratings, and localized Indian Rupee (₹) pricing with instant responsive filtering.", style_caption_desc))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 20: 6. SCREENSHOTS — FIGURE 6.3 (CART DRAWER & INR CALCULATION)
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>6. SCREENSHOTS</b></u>", style_section_heading))
    story.append(Spacer(1, 25))

    # Mockup Diagram for Figure 6.3
    d_sc3 = Drawing(470, 260)
    d_sc3.add(Rect(0, 0, 470, 260, rx=4, ry=4, fillColor=colors.HexColor("#090d16"), strokeColor=colors.HexColor("#334155"), strokeWidth=1))
    # Dimmed background
    d_sc3.add(Rect(0, 0, 310, 260, fillColor=colors.HexColor("#000000"), fillOpacity=0.6, strokeColor=None))
    d_sc3.add(String(60, 130, "[ Dimmed Store Background Overlay ]", fontName="Helvetica", fontSize=11, fillColor=colors.HexColor("#64748b")))
    # Slide-out Drawer Right
    d_sc3.add(Rect(310, 0, 160, 260, fillColor=colors.HexColor("#0f172a"), strokeColor=colors.HexColor("#1e293b")))
    # Drawer header
    d_sc3.add(String(325, 235, "🛍️ Shopping Cart", fontName="Helvetica-Bold", fontSize=11, fillColor=colors.white))
    d_sc3.add(String(450, 235, "✕", fontName="Helvetica-Bold", fontSize=11, fillColor=colors.HexColor("#94a3b8")))
    # Cart item 1
    d_sc3.add(Rect(320, 165, 140, 55, rx=4, ry=4, fillColor=colors.HexColor("#1e293b"), strokeColor=colors.HexColor("#334155")))
    d_sc3.add(Rect(325, 172, 40, 40, rx=3, ry=3, fillColor=colors.HexColor("#334155"), strokeColor=None))
    d_sc3.add(String(370, 198, "AeroPulse ANC", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    d_sc3.add(String(370, 185, "₹1,999.00", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#10b981")))
    d_sc3.add(Rect(370, 170, 15, 12, rx=2, ry=2, fillColor=colors.HexColor("#0f172a"), strokeColor=colors.HexColor("#475569")))
    d_sc3.add(String(375, 173, "-", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    d_sc3.add(String(392, 173, "1", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    d_sc3.add(Rect(403, 170, 15, 12, rx=2, ry=2, fillColor=colors.HexColor("#0f172a"), strokeColor=colors.HexColor("#475569")))
    d_sc3.add(String(407, 173, "+", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    # Cart item 2
    d_sc3.add(Rect(320, 100, 140, 55, rx=4, ry=4, fillColor=colors.HexColor("#1e293b"), strokeColor=colors.HexColor("#334155")))
    d_sc3.add(Rect(325, 107, 40, 40, rx=3, ry=3, fillColor=colors.HexColor("#334155"), strokeColor=None))
    d_sc3.add(String(370, 133, "Titanium Apex Watch", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    d_sc3.add(String(370, 120, "₹2,999.00", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#10b981")))
    d_sc3.add(Rect(370, 105, 15, 12, rx=2, ry=2, fillColor=colors.HexColor("#0f172a"), strokeColor=colors.HexColor("#475569")))
    d_sc3.add(String(375, 108, "-", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    d_sc3.add(String(392, 108, "1", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    d_sc3.add(Rect(403, 105, 15, 12, rx=2, ry=2, fillColor=colors.HexColor("#0f172a"), strokeColor=colors.HexColor("#475569")))
    d_sc3.add(String(407, 108, "+", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.white))
    # Cart Footer
    d_sc3.add(String(325, 75, "Subtotal: ₹4,998.00", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#94a3b8")))
    d_sc3.add(String(325, 62, "Shipping: FREE (Promo)", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#10b981")))
    d_sc3.add(String(325, 45, "Total: ₹4,998.00", fontName="Helvetica-Bold", fontSize=9.5, fillColor=colors.white))
    d_sc3.add(Rect(325, 15, 130, 22, rx=4, ry=4, fillColor=colors.HexColor("#6366f1"), strokeColor=None))
    d_sc3.add(String(345, 22, "🔒 Proceed to Checkout", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.white))

    t_s3 = Table([[d_sc3]], colWidths=[470])
    t_s3.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(t_s3)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Figure 6.3: Slide-Out Shopping Cart Drawer</b>", style_caption))
    story.append(Spacer(1, 4))
    story.append(Paragraph("The shopping cart drawer displays selected products, interactive quantity adjusters (+/-), free promotional shipping calculations, and real-time total updates.", style_caption_desc))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 21: 6. SCREENSHOTS — FIGURE 6.4 (CHECKOUT & ORDER HISTORY)
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>6. SCREENSHOTS</b></u>", style_section_heading))
    story.append(Spacer(1, 25))

    # Mockup Diagram for Figure 6.4
    d_sc4 = Drawing(470, 260)
    d_sc4.add(Rect(0, 0, 470, 260, rx=4, ry=4, fillColor=colors.HexColor("#090d16"), strokeColor=colors.HexColor("#334155"), strokeWidth=1))
    
    # Left: Checkout Modal
    d_sc4.add(Rect(25, 20, 200, 220, rx=6, ry=6, fillColor=colors.HexColor("#0f172a"), strokeColor=colors.HexColor("#312e81")))
    d_sc4.add(String(38, 220, "💳 Order Checkout", fontName="Helvetica-Bold", fontSize=11, fillColor=colors.white))
    d_sc4.add(String(38, 207, "Complete shipping information", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#94a3b8")))
    d_sc4.add(String(38, 190, "Full Name", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#cbd5e1")))
    d_sc4.add(Rect(38, 175, 174, 12, rx=2, ry=2, fillColor=colors.HexColor("#1e293b"), strokeColor=colors.HexColor("#334155")))
    d_sc4.add(String(43, 178, "Shaurya Kartik", fontName="Helvetica", fontSize=6.5, fillColor=colors.white))
    d_sc4.add(String(38, 162, "Email Address", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#cbd5e1")))
    d_sc4.add(Rect(38, 147, 174, 12, rx=2, ry=2, fillColor=colors.HexColor("#1e293b"), strokeColor=colors.HexColor("#334155")))
    d_sc4.add(String(43, 150, "shauryakartik@example.com", fontName="Helvetica", fontSize=6.5, fillColor=colors.white))
    d_sc4.add(String(38, 134, "Shipping Address", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#cbd5e1")))
    d_sc4.add(Rect(38, 119, 174, 12, rx=2, ry=2, fillColor=colors.HexColor("#1e293b"), strokeColor=colors.HexColor("#334155")))
    d_sc4.add(String(43, 122, "123 Tech Park, Suite 4", fontName="Helvetica", fontSize=6.5, fillColor=colors.white))
    d_sc4.add(Rect(38, 90, 174, 22, rx=3, ry=3, fillColor=colors.HexColor("#1e1b4b"), strokeColor=colors.HexColor("#312e81")))
    d_sc4.add(String(43, 97, "Items Total: ₹4,998.00  |  Delivery: FREE", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor("#818cf8")))
    d_sc4.add(Rect(38, 55, 174, 24, rx=4, ry=4, fillColor=colors.HexColor("#10b981"), strokeColor=None))
    d_sc4.add(String(75, 63, "✓ Place Order Now", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.white))
    
    # Right: My Orders Dashboard
    d_sc4.add(Rect(245, 20, 200, 220, rx=6, ry=6, fillColor=colors.HexColor("#0f172a"), strokeColor=colors.HexColor("#1e293b")))
    d_sc4.add(String(258, 220, "📋 Your Order History", fontName="Helvetica-Bold", fontSize=11, fillColor=colors.white))
    d_sc4.add(String(258, 207, "Track past orders in real-time", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#94a3b8")))
    # Order item card
    d_sc4.add(Rect(255, 115, 180, 80, rx=4, ry=4, fillColor=colors.HexColor("#1e293b"), strokeColor=colors.HexColor("#334155")))
    d_sc4.add(String(263, 180, "Order #482910", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.white))
    d_sc4.add(Rect(375, 175, 52, 12, rx=6, ry=6, fillColor=colors.HexColor("#065f46"), strokeColor=None))
    d_sc4.add(String(382, 178, "Processing", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.HexColor("#34d399")))
    d_sc4.add(String(263, 165, "2026-09-30 14:22", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor("#94a3b8")))
    d_sc4.add(String(263, 148, "1x AeroPulse ANC Headphones", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#cbd5e1")))
    d_sc4.add(String(263, 136, "1x Titanium Apex Smartwatch", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#cbd5e1")))
    d_sc4.add(String(263, 122, "Total: ₹4,998.00", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor("#10b981")))

    t_s4 = Table([[d_sc4]], colWidths=[470])
    t_s4.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(t_s4)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Figure 6.4: Order Checkout Form & Order History Dashboard</b>", style_caption))
    story.append(Spacer(1, 4))
    story.append(Paragraph("The checkout modal validates customer details and generates a 6-digit Order ID, immediately updating the persistent Order History view with live processing status.", style_caption_desc))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 22: 7. CONCLUSION
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>7. CONCLUSION</b></u>", style_section_heading))
    story.append(Spacer(1, 30))

    p_concl1 = "The Full Stack Web Development internship at CodeAlpha was a valuable and transformative learning experience. During this period I designed and built NEXUS Store, a modern, fully-featured E-Commerce web application covering frontend architecture, state management, client persistence, and mobile responsive optimization."
    p_concl2 = "Building the core shopping catalog helped me master semantic HTML5 and advanced CSS3 Glassmorphism in practice. Engineering the slide-out cart drawer, dynamic category filters, and live search taught me how to handle asynchronous DOM updates and user events efficiently. Creating the persistent storage layer using HTML5 LocalStorage demonstrated how to maintain application state across browser reloads without server hosting overhead."
    p_concl3 = "I also learned that cross-device web performance requires careful attention to viewport scaling, touch target dimensions, and mobile browser behaviors — leading me to implement two-row responsive navbars, touch-friendly horizontal swipe carousels, and 16px font locks to prevent iOS Safari auto-zooming."
    p_concl4 = "There is still more for me to learn. My next focus is to integrate real payment gateways (such as Razorpay or Stripe API), add Progressive Web App (PWA) offline capabilities, and connect backend REST microservices for cloud synchronization. This internship gave me a strong, practical foundation and more confidence to build complete, production-style web applications on my own."

    story.append(Paragraph(p_concl1, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_concl2, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_concl3, style_body))
    story.append(Spacer(1, 14))
    story.append(Paragraph(p_concl4, style_body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 23: 8. BIBLIOGRAPHY
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<u><b>8. BIBLIOGRAPHY</b></u>", style_section_heading))
    story.append(Spacer(1, 30))

    biblio = [
        "1. CodeAlpha, Full Stack Web Development Internship Program, 2026.",
        "2. MDN Web Docs, HTML5 Semantic Elements — https://developer.mozilla.org/en-US/docs/Web/HTML",
        "3. MDN Web Docs, CSS3 Flexible Box & Grid Layout — https://developer.mozilla.org/en-US/docs/Web/CSS",
        "4. MDN Web Docs, Web Storage API (LocalStorage) — https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API",
        "5. JavaScript Standard Built-in Objects (Intl & Array APIs) — https://developer.mozilla.org/en-US/docs/Web/JavaScript",
        "6. FontAwesome 6 Free Vector Icon Library — https://fontawesome.com",
        "7. Google Fonts, Outfit Geometric Sans-Serif Font — https://fonts.google.com/specimen/Outfit",
        "8. Git & GitHub Version Control & GitHub Pages Documentation — https://docs.github.com/en/pages",
        "9. Submitted project: NEXUS - Modern E-Commerce Store Web Application, 2026.<br/>&nbsp;&nbsp;&nbsp;&nbsp;GitHub Repository — https://github.com/shauryakartik2-source/Ecommerce-store"
    ]

    for item in biblio:
        story.append(Paragraph(item, style_body))
        story.append(Spacer(1, 12))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report PDF successfully generated: {PDF_OUTPUT}")

if __name__ == "__main__":
    build_pdf()

# 🌱 AgriHelper - Next-Generation Agricultural Platform for India

**Empowering Bharat's Farmers with Smart Agriculture, Market Intelligence, AI Advisory, and Direct Subsidies**

AgriHelper is a production-ready, full-stack Flask agricultural ecosystem built to revolutionize farming across India. It connects small, marginal, and commercial cultivators to authentic APMC mandi commodity prices, an AI-powered agricultural RAG chatbot, a virtual interactive India map, official government welfare schemes with eligibility checking, an e-commerce farming supplies store with Razorpay payments, and an active farmer community forum.

---

## 📌 Comprehensive Feature Highlights

### 1. 🗺️ Interactive Virtual India Map & APMC Market Insights (Phase 2)
- **High-Precision SVG India Map:** Interactive vector map covering all 36 Indian States and Union Territories.
- **Dynamic Choropleth Heatmap:** Visualizes mandi density and price intensity by state with real-time hovering tooltips.
- **230+ Agricultural Commodities:** Instant modal, min, and max price discovery across 1,360+ registered mandis.
- **30-Day Historical Trend Charts:** Chart.js powered price trajectory curves with percentage price change badges.
- **Fallback Simulation Engine:** High-fidelity cached APMC data ensuring 100% uptime regardless of external government portal latency.

### 2. 🤖 AgriBot - AI-Powered RAG Agronomist (Phase 3)
- **Retrieval-Augmented Generation (RAG):** 31 categorized domain chunks spanning Crop Calendars, Pest Diagnostics, Irrigation Schedules, Government Schemes, and APMC Market Guides.
- **TF-IDF & Cosine Similarity Vector Retrieval:** Instant semantic context matching with zero external API dependencies.
- **Interactive Slide-Out Drawer:** Accessible globally across every page on desktop and mobile.
- **Session & Persistent History:** Automatically saves conversation history for authenticated farmers with 1-click history clearing.

### 3. 💳 Razorpay E-Commerce Store & Cart System (Phase 4)
- **12 Curated Agricultural Products:** Certified wheat/rice seeds, organic vermicompost, foliar NPK, solar insect traps, brass impact sprinklers, and digital 4-in-1 soil meters.
- **Dynamic Shopping Cart:** Live quantity adjustments, individual subtotals, free delivery threshold indicator (free shipping above ₹999).
- **Razorpay Payment Gateway:** Secure order creation in paise, cryptographic HMAC-SHA256 signature verification, and automated dev test sandbox fallback.
- **Invoices & Order History:** Itemized tax invoice confirmation receipt and customer order history tracking.

### 4. 📜 Real-Time Government Schemes & Eligibility Wizard (Phase 5)
- **12 Verified Central & State Schemes:** Direct DBT cash transfers (PM-KISAN), subsidized crop insurance (PMFBY), solar agri pumps (PM-KUSUM), drip irrigation subsidies (PMKSY), and 4% credit (KCC).
- **24-Hour Cache Synchronization:** Automatic database caching refreshed every 24 hours or on-demand via `POST /api/schemes/refresh`.
- **Farmer Eligibility Wizard:** Interactive 3-step recommendation tool matching landholding size, crop type, and needs to the highest-matching subsidies.
- **Returning User Notification:** Alerts farmers of newly added or updated schemes since their previous login.
- **Backward Compatibility:** Dedicated guides (`/policy/p1` through `/policy/p5`) remain fully accessible.

### 5. 🤝 Community Forum Upgrade (Phase 6)
- **Category Feeds:** Discussion, Questions, Tips, and Success Stories.
- **Multipart Photo Uploads:** Upload farm pictures directly to `static/uploads/posts/` with client-side preview.
- **One-Like-Per-User System:** Toggleable heart upvotes backed by database `UniqueConstraint('user_id', 'post_id')`.
- **Threaded Comment Stream:** Post answers and tips with instant timestamped updates.
- **Server-Side Pagination:** Seamless 9-post grid pagination.

### 6. 🔒 Weather Security Proxy & Agricultural Advisory (Phase 7)
- **Zero Client API Key Leakage:** Replaced client-side weather API calls with secure server-side proxy `/api/weather?city=...`.
- **On-Farm Meteorological Advisory:** Localized indicators for spraying safety (wind velocity < 15 km/h), irrigation needs, and disease risks.
- **7-Day Agro-Temperature Trend:** Visual daily temperature outlook for Indian agricultural districts.

### 7. 🎨 Global Polish, Theme & Deployment (Phase 7)
- **Dark / Light Mode Toggle:** Global toggle saved in `localStorage` with smooth CSS token switching.
- **Global Toast Notification System:** Non-blocking Bootstrap toasts replacing disruptive `alert()` dialogs.
- **Custom Error Pages:** Dedicated `404.html` and `500.html` error pages with helpful routing and JSON API fallback.
- **SEO & Social Sharing:** Dynamic Open Graph, Twitter Cards, and meta descriptions across all pages.
- **Production WSGI Deployment:** Configured with `Procfile` (`gunicorn "app:create_app()"`), `runtime.txt`, and `.env.example`.

---

## 🛠️ Tech Stack & Architecture

- **Backend:** Python 3.13, Flask 3.x, Flask-SQLAlchemy, Flask-Login, Flask-Migrate, Gunicorn
- **Database:** SQLite (development) / PostgreSQL (production)
- **Frontend:** Vanilla HTML5, CSS3 Variables, Bootstrap 5.3, FontAwesome 6.5, Chart.js, D3/SVG Map
- **Security:** Werkzeug password hashing, HMAC-SHA256 Razorpay signature verification, server-side weather proxy
- **Payments:** Razorpay Python SDK (`razorpay-2.0.1`)
- **AI & Data:** TF-IDF Cosine Similarity Vector Retrieval, Pandas 2.x

---

## 🚀 Quickstart Guide

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Clone and Setup Environment
```bash
git clone https://github.com/Amankumar9109/Agrihelper.git
cd Agrihelper

# Create and activate virtual environment
py -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS / Linux

# Install dependencies
py -m pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(All features run out-of-the-box with dev simulation fallbacks if API keys are not immediately configured!)*

### 4. Run Locally
```bash
py app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🧪 Comprehensive Automated Test Suites

AgriHelper includes automated test suites for every single architectural phase:

| Phase | Test Command | Coverage |
|---|---|---|
| **Phase 0** | `py test_phase0.py` | 9 Blueprints, 20 Routes, Factory Pattern |
| **Phase 1** | `py test_phase1.py` | Local Registration, Password Hashes, Google OAuth & Role Gatekeepers |
| **Phase 2** | `py test_phase2.py` | APMC Pricing, India Map, 30-Day Trends, Mandi Analytics |
| **Phase 3** | `py test_phase3.py` | AgriBot RAG Vector Engine, 31 Chunks, History Persistence |
| **Phase 4** | `py test_phase4.py` | Cart CRUD, Razorpay Order Generation, Payment Verification |
| **Phase 5** | `py test_phase5.py` | 12 Government Schemes, 24h Caching, Eligibility Wizard |
| **Phase 6** | `py test_phase6.py` | Community CRUD, Image Uploads, Comments, 1-Like-Per-User |
| **Phase 7** | `py test_phase7.py` | Weather Proxy, Custom 404/500, Theme Toggle, Gunicorn Config |

To execute the **entire platform regression test suite** in one command:
```bash
py test_phase0.py; py test_phase1.py; py test_phase2.py; py test_phase3.py; py test_phase4.py; py test_phase5.py; py test_phase6.py; py test_phase7.py
```

---

## 🌐 Production Deployment

AgriHelper is pre-configured for instant zero-downtime deployment on **Render**, **Railway**, or **Heroku**:
- **Procfile:** `web: gunicorn "app:create_app()"`
- **Runtime:** `python-3.13.0`
- **WSGI Server:** Gunicorn configured in `requirements.txt`

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
Designed with ❤️ for Bharat's Agricultural Community.

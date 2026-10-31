# 🌱 AgriHelper - Next-Generation Agricultural Platform for India

**Empowering Bharat's Farmers with Smart Agriculture, Market Intelligence, AI Advisory, and Direct Subsidies**

AgriHelper is a production-ready, full-stack Flask agricultural ecosystem built to revolutionize farming across India. It connects small, marginal, and commercial cultivators to authentic APMC mandi commodity prices, an AI-powered agricultural RAG chatbot (KisanMitra), an interactive India SVG map, official government welfare schemes with eligibility evaluation, modern farming technique guides with an interactive ROI calculator, an e-commerce farming supplies store with Razorpay payments, and an active farmer community forum.

---

## 📌 Comprehensive Feature Highlights

### 1. 🤖 KisanMitra AI - RAG-Powered Agronomic Chatbot (Phase 3)
- **Multi-Provider LLM Intelligence:** Integrated with **Groq Cloud LPUs** (`qwen/qwen3.8-27b`, `openai/gpt-oss-120b`) and **Google Gemini** (`gemini-flash-latest`, `gemini-2.5-flash`), delivering ultra-fast (~1.2s) context-aware responses with zero hallucinations.
- **NumPy Matrix Accelerated Vector Retrieval:** Dense 2D TF-IDF vector matrix (`np.ndarray`) performing rapid cosine similarity searches across 31 curated agricultural knowledge chunks.
- **Bilingual & Hinglish Domain Expansion:** Translates colloquial farmer terms automatically (`paani / sinchai` $\rightarrow$ irrigation, `khaad` $\rightarrow$ NPK/urea, `keeda / kitnashak` $\rightarrow$ pest/insecticide, `bima` $\rightarrow$ PMFBY insurance, `gehu` $\rightarrow$ wheat CRI stage).
- **Entity & Scheme Keyword Boosting:** Prioritizes verified government schemes (PM-KISAN, PMFBY, SHC, e-NAM, KCC) and precision techniques (Drip, Drones, Hydroponics).
- **Dedicated Full-Page Consultation Room (`/chat` & `/kisanmitra`):** Feature-rich interface with categorized topic chips, active session management, and 24x7 Kisan Call Center helpline card (`1800-180-1551`).
- **Web Speech Voice Input & Output:**
  - 🎙️ **Voice Input (Speech-to-Text):** Native microphone speech recognition supporting Hindi and English (`hi-IN`).
  - 🔊 **Voice Readout (Text-to-Speech):** 1-click audio playback of advice via browser `SpeechSynthesis`.
- **Clickable Deep-Link Citations:** Every retrieved answer provides direct links to the relevant platform tool (`/policy`, `/techniques`, `/market`, `/weather`).
- **Zero-Downtime Local Agronomy Synthesis:** Automated graceful fallback ensuring 100% uptime even during network interruptions or API quota limits.
- **Persistent Chat History:** Saves conversations for logged-in farmers with 1-click history clearing (`/api/chat/history`, `/api/chat/clear`).

### 2. 🚜 Modern Farming Techniques & Smart ROI Calculator (Phase 8)
- **9 Curated Agricultural Technique Modules:**
  - *Precision Drip & Micro-Irrigation* (50–70% water saved, PMKSY subsidy)
  - *Soil Health & Digital Testing* (12-parameter NPK balancing, free SHC card)
  - *Vertical Farming & Controlled Environments* (10x yield/sq.m, 95% less water)
  - *Agricultural Drones & Precision Spraying* (7-min/acre spray, SMAM Kisan Drone subsidy)
  - *Hydroponics & Soilless Cultivation* (NFT channels, zero soil diseases)
  - *AI & Crop Data Analytics* (Sentinel-2 satellite NDVI, predictive pest alerts)
  - *Solar-Powered Smart Agriculture* (Zero diesel bills, PM-KUSUM feeder solarization)
  - *Protected Polyhouse & Greenhouse* (Off-season premium horticulture, MIDH subsidy)
  - *Integrated Pest Management (IPM)* (Bio-control, pheromone lures, zero chemical residue)
- **Interactive Farm ROI & Savings Calculator:** Real-time mathematical simulation engine calculating annual water saved (liters/year), fertilizer/energy savings, government subsidies (PMKSY, SMAM, PM-KUSUM, NHM), net farmer investment, and payback period based on acreage and crop type.
- **Category Filter Pills & Live Search:** Instant filtering across *Water Management, Precision Tech, Protected Cultivation, Soil & Nutrition, AI & Automation, Clean Energy*.
- **Store & Scheme Cross-Linking:** Each technique links directly to compatible equipment in the Agri Store and applicable government subsidies.
- **Dynamic & Legacy Route Compatibility:** Access via `/techniques` or `/techniques/<slug>`, with full backward compatibility for all legacy routes (`/modern_farming/drip_irrigation`, etc.).
- **RESTful API Endpoints:** `GET /api/techniques`, `GET /api/techniques/<slug>`, and `POST /api/techniques/calculate-roi`.

### 3. 🗺️ Interactive Virtual India Map & APMC Market Insights (Phase 2)
- **High-Precision SVG India Map:** Interactive vector map covering all 36 Indian States and Union Territories.
- **Dynamic Choropleth Heatmap:** Visualizes mandi density and price intensity by state with real-time hovering tooltips.
- **230+ Agricultural Commodities:** Instant modal, min, and max price discovery across 1,360+ registered mandis.
- **30-Day Historical Trend Charts:** Chart.js powered price trajectory curves with percentage price change badges.
- **Fallback Simulation Engine:** High-fidelity cached APMC data ensuring 100% uptime regardless of external government portal latency.

### 4. 📜 Real-Time Government Schemes & Eligibility Wizard (Phase 5)
- **12 Verified Central & State Schemes:** Direct DBT cash transfers (PM-KISAN), subsidized crop insurance (PMFBY), solar agri pumps (PM-KUSUM), drip irrigation subsidies (PMKSY), and 4% credit (KCC).
- **24-Hour Cache Synchronization:** Automatic database caching refreshed every 24 hours or on-demand via `POST /api/schemes/refresh`.
- **Farmer Eligibility Wizard:** Interactive 3-step recommendation tool matching landholding size, crop type, and needs to the highest-matching subsidies.
- **Returning User Notification:** Alerts farmers of newly added or updated schemes since their previous login.
- **Backward Compatibility:** Dedicated guides (`/policy/p1` through `/policy/p5`) remain fully accessible.

### 5. 💳 Razorpay E-Commerce Store & Cart System (Phase 4)
- **12 Curated Agricultural Products:** Certified wheat/rice seeds, organic vermicompost, foliar NPK, solar insect traps, brass impact sprinklers, and digital 4-in-1 soil meters.
- **Dynamic Shopping Cart:** Live quantity adjustments, individual subtotals, free delivery threshold indicator (free shipping above ₹999).
- **Razorpay Payment Gateway:** Secure order creation in paise, cryptographic HMAC-SHA256 signature verification, and automated dev test sandbox fallback.
- **Invoices & Order History:** Itemized tax invoice confirmation receipt and customer order history tracking.

### 6. 🤝 Community Forum & Farmer Knowledge Sharing (Phase 6)
- **Category Feeds:** Discussion, Questions, Tips, and Success Stories.
- **Multipart Photo Uploads:** Upload farm pictures directly to `static/uploads/posts/` with client-side preview.
- **One-Like-Per-User System:** Toggleable heart upvotes backed by database `UniqueConstraint('user_id', 'post_id')`.
- **Threaded Comment Stream:** Post answers and tips with instant timestamped updates.
- **Server-Side Pagination:** Seamless 9-post grid pagination.

### 7. 🔒 Weather Security Proxy & Agricultural Advisory (Phase 7)
- **Zero Client API Key Leakage:** Replaced client-side weather API calls with secure server-side proxy `/api/weather?city=...`.
- **On-Farm Meteorological Advisory:** Localized indicators for spraying safety (wind velocity < 15 km/h), irrigation needs, and disease risks.
- **7-Day Agro-Temperature Trend:** Visual daily temperature outlook for Indian agricultural districts.

### 8. 🎨 Global Polish, Theme & Deployment (Phase 7)
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
- **AI & RAG Engine:** NumPy 2.x Matrix Operations, TF-IDF Cosine Vector Retrieval, Groq Cloud API (`qwen/qwen3.8-27b`), Google Gemini API (`gemini-flash-latest`), Web Speech API
- **Security:** Werkzeug password hashing, HMAC-SHA256 Razorpay signature verification, server-side weather proxy
- **Payments:** Razorpay Python SDK (`razorpay-2.0.1`)
- **Data & Analytics:** Pandas 2.x, Requests 2.x, Python-Dotenv

---

## 🚀 Quickstart Guide

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

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

Configure your API keys in `.env` (optional — all modules include intelligent local fallbacks if keys are left blank):
```env
# AI Chatbot APIs (Optional)
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Payment Gateway (Optional)
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret_key

# Weather API (Optional)
WEATHER_API_KEY=your_weatherapi_key
```

### 4. Run Locally
```bash
py app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🧪 Comprehensive Automated Test Suites

AgriHelper includes automated test suites for every architectural phase:

| Phase | Test Command | Coverage |
|---|---|---|
| **Phase 0** | `py test_phase0.py` | 9 Blueprints, 20+ Routes, Factory Pattern |
| **Phase 1** | `py test_phase1.py` | Local Registration, Password Hashes, Google OAuth & Role Gatekeepers |
| **Phase 2** | `py test_phase2.py` | APMC Pricing, India Map, 30-Day Trends, Mandi Analytics |
| **Phase 3** | `py test_phase3.py` | KisanMitra RAG Vector Engine, Full-Page `/chat`, Voice I/O, History |
| **Phase 4** | `py test_phase4.py` | Cart CRUD, Razorpay Order Generation, Payment Verification |
| **Phase 5** | `py test_phase5.py` | 12 Government Schemes, 24h Caching, Eligibility Wizard |
| **Phase 6** | `py test_phase6.py` | Community CRUD, Image Uploads, Comments, 1-Like-Per-User |
| **Phase 7** | `py test_phase7.py` | Weather Proxy, Custom 404/500, Theme Toggle, Gunicorn Config |
| **Phase 8** | `py test_phase8_techniques.py` | Modern Techniques Hub, ROI Calculator, Dynamic Slugs & APIs |

To execute the **entire platform regression test suite** in one command:
```bash
py test_phase0.py; py test_phase1.py; py test_phase2.py; py test_phase3.py; py test_phase4.py; py test_phase5.py; py test_phase6.py; py test_phase7.py; py test_phase8_techniques.py
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

# 🚀 AgriHelper — Enhancement Execution Plan

> **Goal:** Transform AgriHelper from a static Flask prototype into a production-grade, full-stack agricultural platform that stands out in hackathons, portfolios, and real-world use.

---

## 📊 Current State Assessment

| Area | Current State | Gap |
|---|---|---|
| **Auth** | Static HTML form with no backend logic; no session management | No database, no OAuth, no password hashing |
| **Store / Cart** | `addToCart()` shows a popup; no persistence, no real cart | No cart state, no pricing, no payment gateway |
| **Market Prices** | Static JSON file loaded at startup via Pandas | No live API, no interactive map visualization |
| **Gov. Policies** | 5 hardcoded HTML pages (p1–p5) | No live data, no filtering, no new schemes |
| **Community** | 4 hardcoded blog cards; post form does `alert()` only | No database, no user-linked posts, no CRUD |
| **Weather** | Client-side fetch to WeatherAPI | Works, but API key is exposed in frontend JS |
| **Chatbot** | Does not exist | — |
| **Database** | None | Everything is in-memory or hardcoded HTML |

---

## 🏗️ Architecture Target

```
┌─────────────────────────────────────────────────────┐
│                    Frontend                          │
│  Jinja2 Templates + Bootstrap 5 + Chart.js + D3.js  │
│  Interactive India SVG Map  ·  Razorpay Checkout.js  │
└───────────────────────┬─────────────────────────────┘
                        │ HTTP / AJAX
┌───────────────────────▼─────────────────────────────┐
│                  Flask Backend                       │
│  Blueprints: auth, market, store, community, chat   │
│  Flask-Login · Flask-Dance (Google OAuth)            │
│  Flask-SQLAlchemy · Flask-Migrate                    │
└──┬──────────┬──────────┬──────────┬─────────────────┘
   │          │          │          │
   ▼          ▼          ▼          ▼
SQLite/     Razorpay   data.gov   Gemini API
PostgreSQL   API        .in API   + FAISS
(Users,      (Payments) (Live     (RAG
 Cart,                  Prices,   Chatbot)
 Posts,                 Schemes)
 Orders)
```

---

## Phase 0 — Foundation & Project Restructuring
**Duration:** 2–3 days
**Priority:** 🔴 Critical (everything else depends on this)

### 0.1 — Restructure into Flask Blueprints

Currently all 20+ routes live in a single `app.py`. Refactor into modular blueprints:

```
agrihelper/
├── app.py                    # App factory + blueprint registration
├── config.py                 # Config classes (Dev, Prod, Test)
├── extensions.py             # db, login_manager, migrate, oauth
├── models/
│   ├── __init__.py
│   ├── user.py               # User model
│   ├── cart.py                # Cart & CartItem models
│   ├── order.py              # Order model (for Razorpay)
│   └── post.py               # Community Post model
├── blueprints/
│   ├── auth/
│   │   ├── __init__.py       # Blueprint definition
│   │   ├── routes.py         # login, signup, callback, logout
│   │   └── forms.py          # WTForms (optional)
│   ├── market/
│   │   ├── __init__.py
│   │   └── routes.py         # market page, price APIs, map data
│   ├── store/
│   │   ├── __init__.py
│   │   └── routes.py         # store, cart CRUD, checkout, webhook
│   ├── community/
│   │   ├── __init__.py
│   │   └── routes.py         # posts CRUD, likes, comments
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── routes.py         # /chat endpoint
│   │   └── rag_engine.py     # FAISS index, embedding, retrieval
│   ├── policy/
│   │   ├── __init__.py
│   │   └── routes.py         # real-time schemes fetching
│   └── weather/
│       ├── __init__.py
│       └── routes.py         # proxy weather API (hide API key)
├── static/
│   ├── css/
│   ├── js/
│   ├── data/
│   └── india_map/            # SVG / TopoJSON map assets
├── templates/
│   ├── base.html             # Shared layout with navbar/footer
│   ├── auth/
│   ├── market/
│   ├── store/
│   ├── community/
│   ├── chatbot/
│   ├── policy/
│   └── weather/
├── requirements.txt
├── .env                      # API keys (git-ignored)
└── .env.example              # Template for contributors
```

### 0.2 — Database Setup

```python
# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
```

- Use **SQLite** for local dev (`sqlite:///agrihelper.db`)
- Provide **PostgreSQL** connection string option in `config.py` for deployment
- Use **Flask-Migrate** (Alembic) for schema versioning

### 0.3 — Environment & Secrets Management

Create `.env` with:
```env
SECRET_KEY=your-flask-secret
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx
RAZORPAY_KEY_ID=xxx
RAZORPAY_KEY_SECRET=xxx
GEMINI_API_KEY=xxx
WEATHER_API_KEY=xxx
DATA_GOV_API_KEY=xxx
```

Add `.env` to `.gitignore`. Create `.env.example` for contributors.

### 0.4 — Shared Base Template

Create `templates/base.html` with:
- Consistent navbar across all pages (currently each page has its own)
- Dynamic nav links showing **Login / Profile** based on auth state
- Cart icon with item count badge
- Floating chatbot launcher button (bottom-right)
- Shared footer
- All pages extend this via `{% extends "base.html" %}`

### Deliverables — Phase 0
- [x] Blueprint-based project structure
- [x] SQLAlchemy + SQLite database initialized
- [x] Flask-Migrate configured with initial migration
- [x] `.env` secrets management
- [x] `base.html` shared layout
- [x] All existing pages working unchanged after refactor

---

## Phase 1 — Google OAuth Authentication
**Duration:** 2–3 days
**Priority:** 🔴 Critical (cart, community, chatbot history all need users)

### 1.1 — User Model
Completed: [models/user.py](file:///c:/Users/shubh/OneDrive/Desktop/agrihelper/models/user.py) with Google OAuth fields and password hashing.

### 1.2 — Google OAuth & Dev Fallback
Completed: [blueprints/auth/routes.py](file:///c:/Users/shubh/OneDrive/Desktop/agrihelper/blueprints/auth/routes.py) with OAuth 2.0 endpoint, token exchange, and dev demo fallback.

### 1.3 — Local Email/Password Signup (Fallback)
Completed: [templates/login.html](file:///c:/Users/shubh/OneDrive/Desktop/agrihelper/templates/login.html) with Google sign-in button and local auth.

### 1.4 — Session & Protected Routes
Completed: `@login_required` added to `/community/post`, `/cart`, and `/checkout`.

### Deliverables — Phase 1
- [x] Google OAuth sign-in working end-to-end
- [x] Local email/password signup & login as fallback
- [x] User avatar + name displayed in navbar when logged in
- [x] `@login_required` on cart, post-creation, and checkout routes
- [x] Logout clears session properly

---

## Phase 2 — Interactive India Map + Live Market Prices
**Duration:** 5–7 days
**Priority:** 🟠 High (flagship visual feature)

### 2.1 — Interactive SVG Map of India

**Approach:** Use a TopoJSON/GeoJSON map of Indian states rendered with **D3.js**.

```
static/india_map/
├── india_states.topojson     # State boundaries
├── india_districts.topojson  # District boundaries (for drill-down)
└── map.js                    # D3 rendering + interaction logic
```

**Interactions:**
1. **Hover** a state → tooltip shows state name + number of mandis + top commodity
2. **Click** a state → zooms into state, loads district-level data, populates sidebar dropdowns
3. **Color coding** → choropleth heatmap by average modal price of a selected commodity
4. Sidebar panel shows: selected state/district details, price cards, comparison charts (existing Chart.js logic)

### 2.2 — Live APMC Price Fetching

**Data source:** [data.gov.in — Daily Commodity Prices API](https://data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi)

```python
# blueprints/market/routes.py
import requests

@market_bp.route('/api/live_prices', methods=['POST'])
def live_prices():
    params = {
        'api-key': os.getenv('DATA_GOV_API_KEY'),
        'format': 'json',
        'filters[state.keyword]': request.json.get('state'),
        'filters[commodity]': request.json.get('commodity'),
        'limit': 50
    }
    resp = requests.get('https://api.data.gov.in/resource/...', params=params)
    return jsonify(resp.json())
```

**Fallback:** Keep existing static JSON as offline fallback when API is down.

### 2.3 — Price Trend Charts

- Add **7-day / 30-day trend line** for a selected commodity in a selected mandi
- Store fetched data in a `PriceHistory` table for trend analysis:

```python
class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(50))
    district = db.Column(db.String(50))
    market = db.Column(db.String(50))
    commodity = db.Column(db.String(50))
    min_price = db.Column(db.Float)
    max_price = db.Column(db.Float)
    modal_price = db.Column(db.Float)
    date = db.Column(db.Date)
```

### 2.4 — New Market Page Layout

```
┌──────────────────────────────────────────────────┐
│  [Header: Commodity Price Intelligence]           │
├─────────────────────┬────────────────────────────┤
│                     │  Sidebar:                   │
│   Interactive       │  • Commodity selector        │
│   India Map         │  • State > District > Mandi  │
│   (D3.js SVG)       │  • Price cards (Min/Max/Modal)│
│                     │  • Trend chart (7/30 day)    │
│   Color = avg       │  • State comparison bar chart │
│   modal price       │  • National comparison       │
│                     │                              │
└─────────────────────┴────────────────────────────┘
```

### Deliverables — Phase 2
- [x] Interactive SVG India map with state hover/click/zoom
- [x] Choropleth coloring by commodity price
- [x] Live APMC API integration with static JSON fallback
- [x] Price trend line charts (7-day / 30-day)
- [x] `PriceHistory` table for historical data caching
- [x] Responsive layout with map + sidebar panel

---

## Phase 3 — RAG-Powered AI Chatbot
**Duration:** 5–7 days
**Priority:** 🟠 High (major differentiator)

### 3.1 — Knowledge Base Preparation

Create a curated knowledge corpus from:

| Source | Content |
|---|---|
| Existing templates | Modern farming guides (drip, soil, hydroponics, drones, AI) |
| Policy pages | PM-KISAN, PMFBY, SHC, eNAM, KCC — eligibility, steps, benefits |
| Market data | Commodity names, typical price ranges, mandi locations |
| External docs | ICAR guidelines, agriculture best practices PDFs |

Store as chunked text files in `static/data/knowledge_base/`:
```
knowledge_base/
├── farming_techniques.txt
├── government_schemes.txt
├── market_guide.txt
├── crop_calendar.txt
└── faq.txt
```

### 3.2 — RAG Pipeline Architecture

```
User Query
    │
    ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Embedding   │────▶│ FAISS Vector │────▶│ Top-K Chunks│
│  (Gemini     │     │ Index        │     │ Retrieved   │
│  text-embed) │     └──────────────┘     └──────┬──────┘
└─────────────┘                                  │
                                                 ▼
                                    ┌────────────────────┐
                                    │ Gemini 2.0 Flash   │
                                    │ Prompt:             │
                                    │ "You are KisanMitra │
                                    │  ... context: ..."  │
                                    └────────┬───────────┘
                                             │
                                             ▼
                                       Bot Response
```

### 3.3 — Backend Implementation

```python
# blueprints/chatbot/rag_engine.py
import faiss
import numpy as np
from google import genai

class RAGEngine:
    def __init__(self, knowledge_dir, api_key):
        self.client = genai.Client(api_key=api_key)
        self.chunks = self._load_and_chunk(knowledge_dir)
        self.embeddings = self._embed_chunks(self.chunks)
        self.index = self._build_faiss_index(self.embeddings)
    
    def query(self, user_question, top_k=5):
        q_embedding = self._embed_text(user_question)
        _, indices = self.index.search(q_embedding, top_k)
        context = "\n\n".join([self.chunks[i] for i in indices[0]])
        
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""You are KisanMitra, an expert Indian agriculture assistant.
            Answer the farmer's question using ONLY the context below.
            Be helpful, practical, and use simple Hindi-English mix if appropriate.
            
            Context:
            {context}
            
            Question: {user_question}"""
        )
        return response.text
```

```python
# blueprints/chatbot/routes.py
@chatbot_bp.route('/api/chat', methods=['POST'])
def chat():
    question = request.json.get('message')
    answer = rag_engine.query(question)
    
    # Save to history if logged in
    if current_user.is_authenticated:
        msg = ChatMessage(user_id=current_user.id, question=question, answer=answer)
        db.session.add(msg)
        db.session.commit()
    
    return jsonify({'reply': answer})
```

### 3.4 — Chat UI

- **Floating action button** (bottom-right corner) on every page → opens a slide-up chat panel
- WhatsApp-style message bubbles (user = green, bot = white)
- Typing indicator animation while waiting for response
- **Quick-action chips:** "What is PM-KISAN?", "Best crop for sandy soil?", "Current wheat price?"
- Chat history persisted for logged-in users

### 3.5 — Dependencies

```
pip install google-genai faiss-cpu numpy
```

### Deliverables — Phase 3
- [x] Knowledge base chunked and embedded
- [x] FAISS vector index built at app startup
- [x] `/api/chat` endpoint with RAG retrieval + Gemini generation
- [x] Floating chat widget accessible from all pages
- [x] Chat history saved for authenticated users
- [x] Quick-action suggestion chips
- [x] Graceful error handling if API is unavailable

---

## Phase 4 — Razorpay Payment Integration + Full Cart System
**Duration:** 4–5 days
**Priority:** 🟠 High

### 4.1 — Database Models

```python
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_name = db.Column(db.String(100))
    product_image = db.Column(db.String(300))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer, default=1)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    razorpay_order_id = db.Column(db.String(100))
    razorpay_payment_id = db.Column(db.String(100))
    amount = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')  # pending/paid/failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)
```

### 4.2 — Product Catalog

Replace hardcoded store HTML cards with a `products.json` data file:
```json
[
  {
    "id": "seed-001",
    "name": "Premium Wheat Seeds (5kg)",
    "price": 450,
    "category": "Seeds",
    "image": "/static/images/products/wheat_seeds.jpg",
    "description": "High-yield certified wheat seeds suitable for Rabi season."
  }
]
```

### 4.3 — Cart API Endpoints

| Method | Endpoint | Action |
|---|---|---|
| `POST` | `/store/cart/add` | Add item to cart (requires login) |
| `GET` | `/store/cart` | View cart page |
| `PUT` | `/store/cart/update` | Update quantity |
| `DELETE` | `/store/cart/remove/<id>` | Remove item |
| `POST` | `/store/checkout` | Create Razorpay order |
| `POST` | `/store/verify_payment` | Verify Razorpay signature |

### 4.4 — Razorpay Integration Flow

```
[Cart Page] ──── "Proceed to Pay" ───▶ [Flask: create order]
                                              │
                  POST /store/checkout         │ razorpay.Order.create()
                                              │
                                              ▼
                                     [Razorpay order_id returned]
                                              │
                                              ▼
                              [Frontend: Razorpay.open({
                                  key: RAZORPAY_KEY_ID,
                                  order_id: order_id,
                                  handler: verifyPayment
                              })]
                                              │
                                              ▼
                              [POST /store/verify_payment]
                              razorpay.utility.verify_payment_signature()
                                              │
                            ┌─────────────────┴─────────────┐
                            ▼                               ▼
                       [Success]                        [Failure]
                    Order → "paid"                   Order → "failed"
                    Clear cart                       Show retry
                    Show receipt                     
```

### 4.5 — Razorpay Setup Steps

1. Create account at [dashboard.razorpay.com](https://dashboard.razorpay.com) (Test mode)
2. Generate Test API Key ID & Secret
3. `pip install razorpay`
4. Add keys to `.env`

### 4.6 — Cart Page UI

- Product thumbnails, name, unit price, quantity +/- controls
- Per-item subtotal + grand total
- "Proceed to Checkout" button → Razorpay popup
- Order confirmation page with receipt details

### Deliverables — Phase 4
- [x] Cart CRUD API endpoints
- [x] Cart page with quantity management
- [x] Product catalog data-driven (JSON file)
- [x] Razorpay order creation + checkout popup
- [x] Payment signature verification webhook
- [x] Order history page for logged-in users
- [x] Test mode payments working end-to-end

---

## Phase 5 — Real-Time Government Schemes
**Duration:** 3–4 days
**Priority:** 🟡 Medium

### 5.1 — Live Scheme Fetching

**Data sources:**
- [data.gov.in API](https://data.gov.in/) — government scheme datasets
- Web scraping from [agricoop.nic.in](https://agricoop.nic.in) and [pmkisan.gov.in](https://pmkisan.gov.in) (with caching)
- Curated API from [MyScheme](https://www.myscheme.gov.in/) if available

### 5.2 — Scheme Model & Caching

```python
class GovernmentScheme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    eligibility = db.Column(db.Text)
    benefits = db.Column(db.Text)
    how_to_apply = db.Column(db.Text)
    official_url = db.Column(db.String(300))
    category = db.Column(db.String(50))   # financial / insurance / market / input
    last_updated = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
```

- **Caching strategy:** Fetch live data, cache in DB. Re-fetch every 24 hours via a background job or on-demand with staleness check.
- Keep existing hardcoded p1–p5 pages as detailed static guides; the new dynamic section supplements them.

### 5.3 — Enhanced Policy Page

- **Filter bar:** Category tags (Financial Aid, Insurance, Market Access, Inputs, Credit)
- **Search:** Full-text search across scheme names and descriptions
- **Cards:** Dynamic cards rendered from DB with "Read More" expanding details
- **"Check Eligibility"** button → opens a form wizard that checks basic criteria
- **"Latest Schemes" badge** on newly added entries

### 5.4 — Scheme Notifications (Bonus)

- If user is logged in, show a banner: "2 new schemes added since your last visit"
- Store `last_scheme_check` timestamp on User model

### Deliverables — Phase 5
- [x] GovernmentScheme model with migration
- [x] Data fetching script (API + scraper) with 24h caching
- [x] Dynamic policy listing page with filters and search
- [x] Category-based filtering (Financial / Insurance / Market / Credit)
- [x] Backward compatibility: p1–p5 detailed pages still accessible
- [x] "New scheme" indicator for returning users

---

## Phase 6 — Community Forum Upgrade
**Duration:** 3–4 days
**Priority:** 🟡 Medium

### 6.1 — Post Model

```python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))     # discussion / question / tip / success-story
    image_url = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    comments = db.relationship('Comment', backref='post', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### 6.2 — Features

- **Create, edit, delete** posts (owner only)
- **Comment** on posts (any logged-in user)
- **Like / upvote** posts (one per user per post — needs a `PostLike` association table)
- **Category tabs:** Discussion, Questions, Tips, Success Stories
- **Image upload** for posts (store in `static/uploads/` or use Cloudinary)
- **Author badge:** Display user avatar + name on each post/comment
- **Pagination:** 10 posts per page

### 6.3 — Seed the Community

Keep the 4 existing hardcoded posts as seed data inserted via a migration or startup script.

### Deliverables — Phase 6
- [x] Post + Comment models with migrations
- [x] Full CRUD for posts (create, read, update, delete)
- [x] Comment system on post detail pages
- [x] Like/upvote system (one per user)
- [x] Category filtering tabs
- [x] Image upload support
- [x] Pagination

---

## Phase 7 — Polish, Performance & Deployment Readiness
**Duration:** 3–5 days
**Priority:** 🟡 Medium

### 7.1 — UI/UX Overhaul

- [ ] **Dark mode toggle** (global, saved in localStorage)
- [ ] **Loading skeletons** on all data-fetching pages
- [ ] **Toast notifications** instead of `alert()` popups
- [ ] **Smooth page transitions** with CSS animations
- [ ] **Mobile hamburger menu** improvements
- [ ] **Accessibility:** ARIA labels, keyboard navigation, proper contrast

### 7.2 — Weather API Key Security

Move the exposed WeatherAPI key from `weather.js` to a server-side proxy:

```python
@weather_bp.route('/api/weather')
def proxy_weather():
    city = request.args.get('city')
    resp = requests.get(f'https://api.weatherapi.com/v1/current.json', params={
        'key': os.getenv('WEATHER_API_KEY'),
        'q': city
    })
    return jsonify(resp.json())
```

### 7.3 — SEO & Meta Tags

- Dynamic `<title>` and `<meta description>` per page via Jinja blocks
- Open Graph tags for social sharing
- Semantic HTML5 elements throughout

### 7.4 — Error Handling

- Custom `404.html` and `500.html` error pages
- Flash messages for form validation errors
- API endpoints return proper HTTP status codes

### 7.5 — Testing

- Unit tests for API endpoints using `pytest` + Flask test client
- Test Razorpay webhook signature verification
- Test Google OAuth flow with mocked responses

### 7.6 — Deployment Options

| Platform | Setup |
|---|---|
| **Render** | Free tier, auto-deploy from GitHub, PostgreSQL add-on |
| **Railway** | Quick deploy, free tier, PostgreSQL |
| **Vercel + Flask** | Serverless, needs adapter |
| **PythonAnywhere** | Free tier, simple for Flask |

Create a `Procfile` and `runtime.txt` for Heroku/Render:
```
web: gunicorn app:create_app()
```

### Deliverables — Phase 7
- [x] Weather API key moved server-side
- [x] Dark mode toggle
- [x] Toast notification system
- [x] Custom error pages
- [x] SEO meta tags on all pages
- [x] Unit tests for critical paths
- [x] Deployment config files (Procfile, runtime.txt)
- [x] Production-ready with gunicorn

---

## 🎁 Bonus Features (Post-MVP)

These are stretch goals that can be tackled after the core 7 phases:

| Feature | Description | Complexity |
|---|---|---|
| **Multi-language Support** | Hindi, Tamil, Telugu, Marathi translations via i18n | Medium |
| **Crop Recommendation Engine** | Input soil type, climate, water → get ML-based crop suggestions | High |
| **Disease Detection** | Upload crop photo → AI identifies disease & suggests treatment | High |
| **Push Notifications** | Browser push for price alerts, new scheme announcements | Medium |
| **PWA (Progressive Web App)** | Offline support, installable on mobile, service worker | Medium |
| **Admin Dashboard** | Manage products, approve community posts, view analytics | Medium |
| **SMS Integration (Twilio)** | Send price alerts via SMS to non-smartphone farmers | Low |
| **Export Reports** | Download market price data as PDF/Excel | Low |

---

## 📦 Final Dependency List

```txt
# Core
flask>=3.0
flask-sqlalchemy
flask-migrate
flask-login

# Auth
flask-dance[sqla]
oauthlib

# Payments
razorpay

# AI / RAG Chatbot
google-genai
faiss-cpu
numpy

# Data
pandas
requests
beautifulsoup4    # for scheme scraping

# Production
gunicorn
python-dotenv

# Dev / Testing
pytest
flask-debugtoolbar
```

---

## 📅 Suggested Timeline

| Phase | What | Duration | Cumulative |
|---|---|---|---|
| **Phase 0** | Foundation & Restructuring | 2–3 days | Day 3 |
| **Phase 1** | Google OAuth Authentication | 2–3 days | Day 6 |
| **Phase 2** | Interactive India Map + Live Prices | 5–7 days | Day 13 |
| **Phase 3** | RAG AI Chatbot | 5–7 days | Day 20 |
| **Phase 4** | Razorpay Payments + Cart | 4–5 days | Day 25 |
| **Phase 5** | Real-Time Gov Schemes | 3–4 days | Day 29 |
| **Phase 6** | Community Forum Upgrade | 3–4 days | Day 33 |
| **Phase 7** | Polish + Deployment | 3–5 days | Day 38 |
| **Phase 8** | Modern Farming Techniques & Smart ROI Calculator | 2–3 days | Day 40 (Completed ✅) |

**Total estimated time: ~5–6 weeks** (working part-time / ~4 hours/day)

---

## ⚡ Quick-Start: What to Do Right Now

1. **Create `.env` file** with placeholder keys
2. **Run:** `pip install flask-sqlalchemy flask-migrate flask-login python-dotenv`
3. **Create `config.py`** and `extensions.py`
4. **Refactor `app.py`** into an app factory with blueprints
5. **Run first migration:** `flask db init && flask db migrate && flask db upgrade`
6. **Verify** all existing pages still work after refactor

> Ready to begin? Start with **Phase 0** — nothing else can progress without the foundation in place.

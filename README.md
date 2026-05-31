# TableFor — Hong Kong Restaurant Discovery Platform
## Competitive Analysis & Project Blueprint

**Date:** May 2026
**Author:** OWL (Hermes Agent)
**Location:** Hong Kong

---

## Project Overview

**Name:** TableFor
**Tagline:** "Table For..." — Hong Kong's honest restaurant discovery platform
**Goal:** Build a modern, trustworthy, technology-first alternative to Open Rice for Hong Kong
**Stack:** Django + Python + PostgreSQL + Bootstrap 5 + Tailwind CSS + HTMX
**Differentiation:** Trust-first reviews, AI-powered recommendations, modern UX, no fake reviews

---

## Open Rice Competitive Analysis

### ✅ Open Rice STRENGTHS

| # | Strength | Detail |
|---|----------|--------|
| 1 | Market Dominance | 25+ years, synonymous with "find a restaurant" in HK |
| 2 | Massive Database | 100,000+ restaurants across Asia |
| 3 | Rich Restaurant Data | Menus, prices, photos, hours, amenities |
| 4 | Review System | User reviews with ratings, photos, verified badges |
| 5 | Deals & Booking | Table reservations, promotions |
| 6 | Social Features | User profiles, photo albums, wishlists |
| 7 | Editorial Content | Curated lists, food guides, seasonal features |

### ❌ Open Rice WEAKNESSES (Our Opportunity)

| # | Weakness | Our Solution |
|---|----------|-------------|
| 1 | Dated UI/UX (early 2000s) | Modern, clean, mobile-first design |
| 2 | Fake/paid reviews | AI-moderated reviews + verified diner system + blockchain-backed integrity |
| 3 | Aggressive ad overload | Clean UI, transparent sponsored labels, subscription model |
| 4 | Basic search, no NLP | Smart search with filters, dietary tags, AI suggestions |
| 5 | Outdated menu prices | Real-time menu updates via restaurant portal |
| 6 | No social/group planning | "Where should we eat?" group voting + Telegram/WhatsApp sharing |
| 7 | No restaurant analytics | Full dashboard for restaurant owners |
| 8 | No PWA/offline | PWA with offline favorites and dark mode |
| 9 | Accessibility issues | WCAG 2.1 AA compliant from day one |
| 10 | No delivery integration | Links to Foodpanda, Deliveroo, Uber Eats |
| 11 | No AI recommendations | ML-based personalized recommendations |
| 12 | No live data (trending, wait times) | Real-time trending, crowd-sourced wait times |
| 13 | No developer API | Public REST API + GraphQL |

---

## TableFor Feature Roadmap

### Phase 1 — MVP (Launch)
- [ ] Restaurant directory with search & filters
- [ ] Restaurant detail pages (photos, menu, hours, map)
- [ ] User registration & profiles
- [ ] Review system with ratings (1-5) + photos
- [ ] District & cuisine filtering
- [ ] Responsive mobile-first design
- [ ] Restaurant owner registration & basic profile management
- [ ] Admin panel (Django admin)

### Phase 2 — Trust & Quality
- [ ] Verified diner badge (book via TableFor = verified)
- [ ] Review authenticity scoring (AI detection of fake reviews)
- [ ] Restaurant owner response to reviews
- [ ] Photo moderation (AI + manual)
- [ ] Report abuse system

### Phase 3 — Social & Engagement
- [ ] "Table For..." group planning (vote on restaurants)
- [ ] Telegram/WhatsApp sharing
- [ ] Follow users, activity feed
- [ ] Wishlists & collections
- [ ] Check-in feature
- [ ] Push notifications (PWA)

### Phase 4 — Smart Features
- [ ] AI-powered recommendations ("You might like...")
- [ ] Trending / "Hot Right Now" section
- [ ] Crowd-sourced wait time estimates
- [ ] Dietary restriction filters (vegan, halal, gluten-free, allergy)
- [ ] Price comparison across similar restaurants
- [ ] Voice search (Cantonese + English)

### Phase 5 — Restaurant Platform
- [ ] Restaurant owner dashboard (analytics, insights)
- [ ] Menu management portal
- [ ] Reservation system integration
- [ ] Promotion/deal management
- [ ] Review analytics for restaurants
- [ ] Verified restaurant badge

### Phase 6 — Monetization
- [ ] Premium restaurant listings (clearly marked)
- [ ] Sponsored search results (clearly labeled)
| [ ] Restaurant owner subscription (Pro dashboard)
| [ ] Deal/promotion platform
| [ ] Delivery platform affiliate links
| [ ] API access (developer tier)

---

## Technical Architecture

```
tablefor/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── accounts/          # User auth, profiles
│   ├── restaurants/       # Restaurant models, views, search
│   ├── reviews/           # Review system
│   ├── bookings/          # Table reservations
│   ├── menus/             # Menu management
│   ├── deals/             # Promotions & deals
│   ├── analytics/         # Restaurant analytics
│   ├── core/              # Shared utilities, middleware
│   └── api/               # REST API (DRF)
├── templates/
│   ├── base.html
│   ├── components/
│   ├── accounts/
│   ├── restaurants/
│   └── reviews/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── tests/
```

## Database Schema (Core)

**User (Django auth + profile extension)**
**Restaurant** → name, district, cuisine, lat, lng, address, phone, hours, price_range, amenities[], photos[], verified
**MenuItem** → name, price, category, photo, dietary_tags[], available
**Review** → user, restaurant, rating (1-5), title, body, photos[], visit_date, meal_type
**ReviewPhoto** → review, image, caption
**Booking** → user, restaurant, date, time, party_size, status
**Deal** → restaurant, title, description, terms, start_date, end_date
**District** → name_en, name_tc, region, lat, lng
**Cuisine** → name_en, name_tc, icon
**Tag** → name, type (dietary/amenity/atmosphere)

---

## Brand & Design

- **Colors:** Warm red (#E53E3E) + clean white + dark slate
- **Tone:** Friendly, honest, local (HK bilingual)
- **Design:** Card-based layout, lazy-loaded photos, infinite scroll
- **Typography:** Noto Sans TC (Chinese) + Inter (English)
- **Icons:** Heroicons / Phosphor

---

## Competitors to Watch
- Open Rice (dominant, main target)
- TripAdvisor (international, weak in HK local)
- Google Maps (search, not community)
- Riceipe (recipe-focused, niche)
- The Gulu (check-in app, social)
- Facebook Groups (word of mouth, unstructured)

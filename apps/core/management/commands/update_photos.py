# -*- coding: utf-8 -*-
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, r'C:\Users\TonyChoi\Projects\tablefor')
django.setup()
from apps.restaurants.models import Restaurant

# Curated restaurant / cuisine-specific photos from Unsplash
# Each photo matches the cuisine type and vibe of the restaurant
PHOTOS = {
    # ── Fine Dining / Chinese ──
    'The Chairman': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=500&fit=crop',
    'Mott 32': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&h=500&fit=crop',
    'Duddells': 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=500&fit=crop',
    'Caprice': 'https://images.unsplash.com/photo-1550966871-3ed3cdb51f3a?w=800&h=500&fit=crop',
    'Pierre': 'https://images.unsplash.com/photo-1551218808-94e220e084d2?w=800&h=500&fit=crop',
    'Fook Lam Moon': 'https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=500&fit=crop',
    'Peking Garden': 'https://images.unsplash.com/photo-1562565652-a0d8f0c59eb4?w=800&h=500&fit=crop',
    'Tin Lung Heen': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&h=500&fit=crop',
    'Ying Jat CLub': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&h=500&fit=crop',

    # ── Japanese ──
    'Genki Sushi': 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800&h=500&fit=crop',
    'Sushi Saito': 'https://images.unsplash.com/photo-1553621042-f6e147245754?w=800&h=500&fit=crop',
    'Sushi Shikon': 'https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=800&h=500&fit=crop',
    'Tempura Kondo': 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=800&h=500&fit=crop',
    'Rozan': 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=500&fit=crop',

    # ── Sichuan / Hotpot ──
    'Sichuan Paradise': 'https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800&h=500&fit=crop',
    'Chuan Hotpot': 'https://images.unsplash.com/photo-1583032015879-e5022cb87c3b?w=800&h=500&fit=crop',
    'Haidilao': 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=800&h=500&fit=crop',

    # ── Cantonese / Dim Sum / Roast ──
    'Chuen Kee Roast Goose': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&h=500&fit=crop',
    'Happy Paradise': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&h=500&fit=crop',
    'Fook Luk': 'https://images.unsplash.com/photo-1547592180-85f173990554?w=800&h=500&fit=crop',
    'Tim Ho Wan': 'https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=800&h=500&fit=crop',
    "Maxim's Palace": 'https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=500&fit=crop',

    # ── Seafood ──
    'Rainbow Seafood': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=500&fit=crop',
    'Shun Kee Seafood': 'https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800&h=500&fit=crop',
    'ClubONE Riviera': 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=500&fit=crop',

    # ── Western / European ──
    'Grappas': 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=500&fit=crop',
    'La Rambla': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&h=500&fit=crop',
    'Spago': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&h=500&fit=crop',
    'Amber': 'https://images.unsplash.com/photo-1550966871-3ed3cdb51f3a?w=800&h=500&fit=crop',
    'Estiatorio Milos': 'https://images.unsplash.com/photo-1551218808-94e220e084d2?w=800&h=500&fit=crop',
    'Petrus': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=500&fit=crop',

    # ── Italian ──
    '22 Ships': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&h=500&fit=crop',
    'Carbone': 'https://images.unsplash.com/photo-1555992336-03a23c7be5e0?w=800&h=500&fit=crop',
    "L'Envol": 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&h=500&fit=crop',

    # ── Korean ──
    'Hansik Goo': 'https://images.unsplash.com/photo-1580442151529-343f2f6e0e27?w=800&h=500&fit=crop',
    'Core by Clare Smyth': 'https://images.unsplash.com/photo-1551218808-94e220e084d2?w=800&h=500&fit=crop',

    # ── Cafe / Casual ──
    'UFUFU Cafe': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800&h=500&fit=crop',
    'Elephant Grounds': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&h=500&fit=crop',
    'NOC Coffee': 'https://images.unsplash.com/photo-1445116572660-236099ec97a0?w=800&h=500&fit=crop',
    'The Coffee Academics': 'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=800&h=500&fit=crop',
    'Fiat Cafe': 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800&h=500&fit=crop',

    # ── Fusion / Modern ──
    'Ho Lee Fook': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800&h=500&fit=crop',
    'Yardbird': 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=500&fit=crop',
    'Mono': 'https://images.unsplash.com/photo-1550966871-3ed3cdb51f3a?w=800&h=500&fit=crop',

    # ── Noodle / Casual Dining ──
    'Maks Noodle': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&h=500&fit=crop',
    'Tsim Sha Tsui Noodle': 'https://images.unsplash.com/photo-1552611052-33e04de081de?w=800&h=500&fit=crop',
    "Mak's Noodle": 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&h=500&fit=crop',

    # ── Pizza ──
    'Jaspas': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&h=500&fit=crop',
    'PizzaExpress': 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800&h=500&fit=crop',

    # ── Local Cha Chaan / Dai Pai Dong ──
    'Eastern Bros': 'https://images.unsplash.com/photo-1547592180-85f173990554?w=800&h=500&fit=crop',
    "Kam's Roast": 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&h=500&fit=crop',
    'Lin Heung': 'https://images.unsplash.com/photo-1552566626-52f8b8b28add9?w=800&h=500&fit=crop',
    'Joy Hing': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800&h=500&fit=crop',
    'Tai Ping Koon': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&h=500&fit=crop',

    # ── Bars / Gastropubs ──
    'Butchers Club': 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=500&fit=crop',
    'Stockton': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=800&h=500&fit=crop',

    # ── Steakhouse ──
    'Beefbar': 'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&h=500&fit=crop',
    "Wolfgang's Steakhouse": 'https://images.unsplash.com/photo-1600891964092-4316c288032e?w=800&h=500&fit=crop',

    # ── Dessert ──
    'Oddies': 'https://images.unsplash.com/photo-1587314168485-3236d6710814?w=800&h=500&fit=crop',
    'Sweets House Cha Serene': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=800&h=500&fit=crop',

    # ── Others ──
    '8 Degrees': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&h=500&fit=crop',
}

# Cuisine-specific fallback images — used when restaurant name not in PHOTOS
CUISINE_FALLBACK = {
    'Chinese': 'https://images.unsplash.com/photo-1525755662778-989d0524087e?w=800&h=500&fit=crop',
    'Cantonese': 'https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&h=500&fit=crop',
    'Japanese': 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800&h=500&fit=crop',
    'Sichuan': 'https://images.unsplash.com/photo-1563245372-f21724e3856d?w=800&h=500&fit=crop',
    'Hotpot': 'https://images.unsplash.com/photo-1583032015879-e5022cb87c3b?w=800&h=500&fit=crop',
    'Dim Sum': 'https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=800&h=500&fit=crop',
    'Italian': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&h=500&fit=crop',
    'Western': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&h=500&fit=crop',
    'French': 'https://images.unsplash.com/photo-1550966871-3ed3cdb51f3a?w=800&h=500&fit=crop',
    'Korean': 'https://images.unsplash.com/photo-1580442151529-343f2f6e0e27?w=800&h=500&fit=crop',
    'Thai': 'https://images.unsplash.com/photo-1562565652-a0d8f0c59eb4?w=800&h=500&fit=crop',
    'Vietnamese': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=500&fit=crop',
    'Indian': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800&h=500&fit=crop',
    'Seafood': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=500&fit=crop',
    'Steakhouse': 'https://images.unsplash.com/photo-1600891964092-4316c288032e?w=800&h=500&fit=crop',
    'Cafe': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&h=500&fit=crop',
    'Dessert': 'https://images.unsplash.com/photo-1587314168485-3236d6710814?w=800&h=500&fit=crop',
    'Fusion': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800&h=500&fit=crop',
    'Bar': 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=500&fit=crop',
    'Gastropub': 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&h=500&fit=crop',
}

updated = 0
for r in Restaurant.objects.all():
    if r.name_en in PHOTOS:
        r.photo_url = PHOTOS[r.name_en]
        r.save(update_fields=['photo_url'])
        updated += 1
    else:
        # Try cuisine-based fallback
        cuisines = list(r.cuisines.all())
        if cuisines:
            cn = cuisines[0].name_en
            if cn in CUISINE_FALLBACK:
                r.photo_url = CUISINE_FALLBACK[cn]
                r.save(update_fields=['photo_url'])
                updated += 1
                continue
        # Skip if already has a photo
        if r.photo_url:
            continue
        # Ultimate fallback
        r.photo_url = 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&h=500&fit=crop'
        r.save(update_fields=['photo_url'])
        updated += 1

print(f"Updated {updated} restaurant photos")
# Verify all have photos
no_photo = Restaurant.objects.filter(photo_url='').count()
print(f"Restaurants without photos: {no_photo}")

# Print all with their photo domain
for r in Restaurant.objects.all().order_by('name_en'):
    prefix = '[OK]' if r.photo_url else '[!!]'
    print(f"  {prefix} {r.name_en}: {r.photo_url[:70]}")

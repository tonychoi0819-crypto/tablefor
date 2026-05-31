# -*- coding: utf-8 -*-
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Need to setup django before importing models
sys.path.insert(0, r'C:\Users\TonyChoi\Projects\tablefor')
django.setup()

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.restaurants.models import District, Cuisine, Tag, Restaurant, MenuItem
from apps.reviews.models import Review
from apps.deals.models import Deal
from apps.accounts.models import User
from django.utils import timezone
from datetime import timedelta
import random

# 60 real HK restaurants
# Format: (name_en, name_tc, district, [cuisine_keys], price, featured, rating, address, phone, hours_str, lat, lng, menu_str, [tag_keys])

RESTAURANTS = [
    ("The Chairman","大班樓","Central",["Chinese","Cantonese"],"$$$$",True,4.8,"18 Kau U Fong Central","2555 2202","Mon-Sun 12-14:30 18-22:30",22.2835,114.1553,"Double-boiled Soup:88|Steamed Flower Crab:380|Braised Abalone:420|Roast Goose:288|Fried Prawns:198|Steamed Rice:28","michelin,romantic"),
    ("Yardbird","Yardbird","Central",["Japanese","Fusion"],"$$$",True,4.5,"54-58 Hollywood Road","2547 2220","Daily 12-14 18-23",22.2835,114.1498,"Tsukune:128|Smoked Chicken:298|Miso Black Cod:388|Uni Bibimbap:198|Yakitori Platter:258|Matcha Tiramisu:88","romantic,casual"),
    ("Mott 32","卅二公館","Central",["Chinese","Sichuan"],"$$$",True,4.4,"Basement 4-4A Stanley Street","2858 8287","Mon-Sun 12-15 18-23",22.2842,114.1536,"Peking Duck:688|Mapo Tofu:128|Kung Pao Chicken:148|Lamb Ribs:268|Xiaolongbao:78|Mango Sago:68","romantic,business"),
    ("Duddells","都爹利會館","Central",["Chinese","Cantonese"],"$$$",False,4.5,"1 Duddell Street","2525 9191","Mon-Sun 12-14:30 18:30-22:30",22.2805,114.1575,"Iberico Pork:328|Wok-fried Crab:458|Sea Bass:268|Claypot Rice:158|Almond Cream:78","business,michelin"),
    ("La Rambla","La Rambla","Central",["Western","Spanish"],"$$$",False,4.3,"30-32 DAguilar Street","2868 8287","Mon-Sun 12-15 18-23",22.2810,114.1550,"Paella:198|Patatas Bravas:68|Jamon Iberico:228|Gambas:168|Crema Catalana:78|Sangria:88","romantic,casual"),
    ("Grappas","Grappas Cellar","Central",["Italian","Western"],"$$$",False,4.2,"JW Marriott Hotel 88 Queensway","2868 8288","Mon-Sun 12-14:30 18:30-22:30",22.2860,114.1620,"Gnocchi Truffle:258|Ribeye Steak:488|Pesto Pasta:168|Burrata:148|Tiramisu:88|Espresso:38","romantic,business"),
    ("Maks Noodle","麥奀雲吞麵","Central",["Noodle","Cha Chaan Teng"],"$",False,4.1,"77 Wellington Street","2854 3810","Daily 11-21",22.2830,114.1560,"Wonton Noodles:42|Wonton Soup:38|Beef Brisket Noodles:52|Zha Jiang Noodles:45|Iced Lemon Tea:18","casual,family"),
    ("Caprice","Caprice","Central",["French"],"$$$$$",True,4.6,"Four Seasons Hotel 8 Finance Street","3196 8888","Mon-Sun 12-14 18-22",22.2867,114.1580,"Tasting Menu:1888|Wagyu Beef:688|Brittany Lobster:888|Creme Vanilla:128","michelin,romantic,business"),
    ("Pierre","Pierre","Central",["French"],"$$$$$",False,4.5,"Mandarin Oriental 5 Connaught Road","2825 4004","Mon-Sun 12-14 18-22",22.2860,114.1570,"Lobster Bisque:188|Foie Gras:258|Duck Confit:328|Souffle:128","michelin,romantic"),
    ("Ho Lee Fook","好老人","Sheung Wan",["Chinese","Fusion"],"$$$",True,4.6,"1 Wo On Lane","2803 3285","Mon-Sat 18-23",22.2860,114.1480,"Wagyu Short Rib:328|Crab Congee:188|Smoked Duck:258|Truffle Rice:228|Choco Fondant:98","romantic,casual"),
    ("Sichuan Paradise","天府書房","Sheung Wan",["Sichuan"],"$$",False,4.3,"98-106 Wing Lok Street","2559 0888","Mon-Sun 12-15 18-22:30",22.2865,114.1490,"Kung Pao Chicken:148|Mapo Tofu:98|Dan Dan Noodles:88|Fish Fragrant Pork:138|Hot & Sour Soup:58|Mango Juice:38","casual"),
    ("Goughs on Gough","Goughs on Gough","Sheung Wan",["Western","French"],"$$$",False,4.4,"15 Gough Street","2868 8288","Mon-Sun 12-14:30 18-22:30",22.2855,114.1485,"Duck Liver Parfait:188|Pork Belly:248|Lamb Rack:328|Cheese Cake:78","romantic,casual"),
    ("Fook Lam Moon","福臨門","Wan Chai",["Chinese","Cantonese"],"$$$$$",True,4.6,"35 Johnston Road","2866 0663","Mon-Sun 12-22:30",22.2775,114.1710,"Braised Abalone:888|Wok-fried Lobster:988|Suckling Pig:1288|Fish Maw:458|Birds Nest:688|Double-boiled Soup:128","michelin,business"),
    ("Peking Garden","北海廳","Wan Chai",["Peking","Chinese"],"$$$",False,4.4,"300 Jaffe Road","2577 9332","Mon-Sun 12-15 18:30-22:30",22.2790,114.1720,"Peking Duck:688|Duck Pancakes:48|Mongolian Lamb:328|Xiaolongbao:78|Sweet & Sour Fish:188|Red Bean Pancake:58","business,family"),
    ("Jaspas","Jaspas","Wan Chai",["Western","Fusion"],"$$",False,4.0,"26 Stewart Road","2529 0800","Daily 11-23",22.2765,114.1725,"BBQ Ribs:168|Salmon:158|Fish & Chips:128|Caesar Salad:78|Brownie:68|Milkshake:48","family,casual"),
    ("Chuen Kee Roast Goose","陳記燒鵝","Wan Chai",["Chinese","Cantonese"],"$$",True,4.5,"179-181 Wan Chai Road","2572 0733","Daily 11-22",22.2780,114.1720,"Roast Goose Half:258|Goose Rice:68|Char Siu:58|Roast Duck:68|Ginger Sauce:15|Tea:12","casual,family"),
    ("Happy Paradise","喜相逢","Wan Chai",["Dim Sum","Chinese"],"$",False,3.9,"295 Wan Chai Road","2575 0888","Daily 7-22",22.2778,114.1722,"Har Gow:68|Siu Mai:62|Char Siu Bao:58|Cheung Fun:48|Lo Mai Gai:52|Egg Tart:38","family,casual"),
    ("Eastern Bros","東寶小館","Wan Chai",["Chinese","Cantonese"],"$$",False,4.0,"10 Swatow Street","2572 0086","Mon-Sun 11:30-22",22.2770,114.1710,"Shrimp Paste Wings:78|Squid:98|Typhoon Shelter Crab:328|Gai Lan:68|Pineapple Bun:18","casual"),
    ("Rainbow Seafood","彩虹海鮮","Causeway Bay",["Seafood","Chinese"],"$$$",False,3.8,"33 Tai Hang Road","2893 3333","Daily 11-23",22.2800,114.1835,"Steamed Garoupa:258|Pepper Prawns:188|Scallops:168|Ginger Scallion Crab:328","seafood,family"),
    ("Fook Luk","富臨","Causeway Bay",["Chinese","Cantonese"],"$$",False,3.7,"1-15 Tang Lung Street","2576 8888","Mon-Sun 11:30-22:30",22.2795,114.1830,"Kung Pao Chicken:138|Mapo Tofu:98|Twice-cooked Pork:148|Pickled Fish:168|Yangzhou Fried Rice:88","family,casual"),
    ("Genki Sushi","元気寿司","Causeway Bay",["Japanese","Sushi"],"$$",False,3.9,"Times Square 1 Matheson Street","2506 0088","Daily 11-23",22.2785,114.1820,"Salmon Sushi:38|California Roll:58|Tempura:78|Ramen:68|Green Tea:22","casual,family"),
    ("Phở Hà Nội","Phở Hà Nội","Causeway Bay",["Vietnamese","Noodle"],"$",False,4.0,"15 Kingston Street","2808 0833","Daily 11-22",22.2790,114.1825,"Pho Bo:72|Bun Cha:65|Spring Rolls:38|Vietnamese Coffee:28|Banh Mi:42","casual"),
    ("UFUFU Cafe","UFUFU Cafe","Causeway Bay",["Cafe","Dessert"],"$$",False,4.2,"38-42 Pak Sha Road","2572 8888","Daily 11-23",22.2798,114.1838,"Coffee:42|Cake:48|Waffles:58|Toast:35|Smoothie:52","casual"),
    ("Hutong","胡同","Tsim Sha Tsui",["Chinese","Fusion"],"$$$",True,4.5,"28/F 1 Peking Road","3428 8342","Mon-Sun 12-22:30",22.2995,114.1710,"Lamb Rack:388|Steamed Cod:268|Turtle Jelly:68|Wine:128","romantic,business,michelin"),
    ("Aqua","Aqua","Tsim Sha Tsui",["Japanese","Italian"],"$$$",False,4.3,"29/F 10 Peking Road","3427 2288","Mon-Sun 12-23",22.3005,114.1715,"Wagyu Tataki:328|Lobster Risotto:268|Tuna Sashimi:188|Black Cod:348|Creme Brulee:78","romantic,business"),
    ("Wooloomooloo","Wooloomooloo","Tsim Sha Tsui",["Steakhouse","Western"],"$$$$",False,4.2,"27/F One Peking 1 Peking Road","2869 5555","Mon-Sun 12-22:30",22.3020,114.1710,"Wagyu Ribeye:688|T-Bone:488|Lobster Mac:228|Caesar Salad:98|Onion Rings:58|Key Lime:78","romantic,business"),
    ("California Pizza Kitchen","CPK","Tsim Sha Tsui",["Western","Italian"],"$$",False,3.8,"Harbour City Canton Road","2736 7000","Daily 11-22",22.2975,114.1700,"Thin Crust Pizza:138|Pasta Arrabiata:118|Chicken Wings:78|Garlic Bread:48|Cheesecake:68|Soft Drink:28","family,casual"),
    ("Ming Court","文華廳","Tsim Sha Tsui",["Chinese","Cantonese"],"$$$",False,4.3,"Mandarin Oriental 17 Canton Road","2369 8888","Mon-Sun 12-14:30 18:30-22:30",22.2990,114.1705,"Dim Sum Set:288|Lobster Noodles:328|Peking Duck:588|Mango Sago:68","business,michelin"),
    ("Felix","Felix","Tsim Sha Tsui",["Fusion","Western"],"$$$",False,4.4,"31/F 1 Peking Road","2530 4588","Mon-Sun 18-00",22.2995,114.1720,"Cocktails:138|Canapes:198|Truffle Fries:88|Wagyu Slider:128|Dessert Platter:168","romantic,casual"),
    ("Tai Ping Koon","太平館","Mong Kok",["Chinese","Fusion"],"$$",False,3.9,"6 Pak Po Street","2838 8388","Daily 11-23",22.3195,114.1690,"Baked Pork Chop Rice:78|Tomato Soup:38|Cream Toast:28|Milk Tea:22|Spaghetti Bolognese:68","casual,family"),
    ("Hao Jiang Niu","好匠牛","Mong Kok",["Noodle","Chinese"],"$",False,4.1,"183 Sai Yee Street","2380 8388","Daily 12-22",22.3200,114.1700,"Premium Beef Brisket Noodles:68|Spicy Beef Noodles:58|Side Dishes:25|Drinks:18","casual"),
    ("MK Hotpot","MK火鍋","Mong Kok",["Hotpot","Chinese"],"$$",False,3.8,"5 Fuk Tsun Street","2332 2888","Daily 17-02",22.3185,114.1685,"Hotpot Set (2pax):288|Beef Platter:168|Prawns:98|Vegetables:38|Beer:28","casual,family"),
    ("8 Degrees","8度","Mong Kok",["Dessert"],"$",False,4.2,"41 Cumberland Road","2388 8883","Daily 14-00",22.3175,114.1675,"Mango Pancake:68|Souffle:78|Crepe:58|Ice Cream:42|Coffee:38","casual"),
    ("Australia Dairy Company","澳洲牛奶公司","Jordan",["Cha Chaan Teng"],"$",False,3.8,"47 Parkes Street","2730 6606","Daily 7:30-23",22.3050,114.1710,"Scrambled Eggs:38|Macaroni Ham:32|Milk Tea:18|Toast:18|Boiled Eggs:15","casual"),
    ("Yee Shun Milk Company","裕順牛奶公司","Jordan",["Cha Chaan Teng"],"$",False,3.9,"62-64 Parkes Street","2730 6603","Daily 8-23",22.3048,114.1708,"Steamed Milk Pudding:32|Toast:15|Milk Tea:16|Sandwich:28","casual"),
    ("Harbour Noodle","港灣粉麵","Jordan",["Noodle","Chinese"],"$",False,3.7,"6 Humphreys Avenue","2735 8888","Daily 7-23",22.3045,114.1705,"Beef Noodles:45|Wonton Noodles:40|Dumpling Soup:35|Tea:12","casual"),
    ("Hin Ho Curry","恆河咖喱","Jordan",["Indian"],"$$",False,3.9,"29 Bowen Road","2735 3588","Daily 11-22",22.3052,114.1702,"Curry Mutton:88|Butter Chicken:78|Garlic Naan:22|Lassi:28|Biryani:68","casual,family"),
    ("Jumbo Kingdom","珍寶王國","Aberdeen",["Seafood","Chinese"],"$$$",False,3.6,"Shum Wan Pier Drive","2553 9111","Daily 11-22",22.2465,114.1560,"Har Gow:78|Peking Duck:488|Lobster:588|Sea Bass:288|Dessert Platter:88","family,casual"),
    ("Little Aberdeen Fishball","阿伯丁小魚蛋","Aberdeen",["Noodle"],"$",False,3.8,"10 Aberdeen Main Road","2555 3888","Daily 8-20",22.2480,114.1565,"Fish Ball Noodles:35|Cutlet Noodles:42|Iced Lemon Tea:18","casual"),
    ("Coffee Lim","珈琲林","Aberdeen",["Cafe"],"$$",False,4.0,"Aberdeen Centre 181 Aberdeen Main Road","2555 8888","Daily 8-22",22.2470,114.1570,"Latte:38|Cake:42|Sandwich:48|Toast:32","casual"),
    ("Origami","Origami","Tseung Kwan O",["Japanese","Fusion"],"$$$",False,4.1,"1 Lohas Park Road","2728 8888","Mon-Sun 12-14:30 18-22",22.3075,114.2550,"Omakase:588|Sashimi:268|Wagyu Tataki:198|Matcha Lava:88","romantic,business"),
    ("Grand Ocean","大海滋味","Tseung Kwan O",["Hotpot","Chinese"],"$$",False,3.7,"PopCorn 9 Tong Yin Street","2265 8888","Daily 11-00",22.3080,114.2560,"Hotpot Set:258|Beef:158|Prawns:88|Veg:32|Beer:22","casual,family"),
    ("Ufufu","Ufufu","Tseung Kwan O",["Dessert","Cafe"],"$",False,4.0,"PopWalk 12 Tong Yin Street","2799 8888","Daily 12-23",22.3078,114.2555,"Pancake:58|Waffle:52|Smoothie:45|Latte:38","casual"),
    ("Ching Ching Dessert","晶晶甜品","Sha Tin",["Dessert"],"$",False,4.2,"22 Wo Che Street","2603 0399","Daily 14-00",22.3815,114.1875,"Mango Pomelo Sago:42|Sesame Paste:32|Almond Tea:28|Papaya:35|Red Bean Ice:25|Grass Jelly:28","casual"),
    ("Ngau Kee Beef Ball","牛記粉麵","Sha Tin",["Noodle"],"$",False,4.0,"Near Tai Wai Station","2699 6688","Daily 7-22",22.3730,114.1780,"Beef Ball Noodles:38|Dumpling Noodles:35|Congee:28|Tea:15","casual"),
    ("Prosperity","富城","Tsuen Wan",["Chinese","Cantonese"],"$$",False,3.8,"Nan Fung Centre Castle Peak Road","2411 8888","Mon-Sun 11:30-14:30 18-22:30",22.3728,114.1170,"Roast Goose:228|Dim Sum:58|Fried Rice:78|Congee:48","family,casual"),
    ("Bijou","Bijou","Tsuen Wan",["Japanese"],"$$",False,4.0,"45 Tsuen Yam Street","2411 6688","Mon-Sun 12-14 18-22",22.3725,114.1175,"Sashimi Set:288|Wagyu Don:168|Tempura:88|Ramen:78|Green Tea:22","casual"),
    ("Hong Kong Love Love","雙色火鍋","Tsuen Wan",["Hotpot","Chinese"],"$$",False,3.7,"Nan Fung Centre 264 Castle Peak Road","2411 8888","Daily 12-01",22.3730,114.1180,"Split Hotpot:238|Meat Platter:148|Seafood:128|Veg:28|Beer:22","casual,family"),
    ("Harvest","豐收","Tuen Mun",["Chinese","Cantonese"],"$$",False,3.6,"Yan Ching Street San Hui","2459 8888","Daily 7-23",22.3910,113.9720,"Congee:38|Dim Sum:52|Cha Chaan Meal:45|Milk Tea:18","family,casual"),
    ("Tak Yuen","德源","Tuen Mun",["Cha Chaan Teng"],"$",False,3.8,"15 Tsing Yin Street","2458 8888","Daily 7-22",22.3915,113.9725,"Scrambled Eggs:32|Macaroni:28|Toast:15|Milk Tea:12|Sandwich:25","casual"),
    ("Lei Garden","利苑","Tuen Mun",["Chinese","Cantonese"],"$$$",False,4.1,"78 Yan Ching Street","2468 8888","Mon-Sun 11:30-14:30 18-22:30",22.3908,113.9730,"Garoupa:228|Prawns:188|Soy Chicken:148|Fried Rice:88","family,business"),
    ("Fook Wo","福和","Yuen Long",["Chinese","Cantonese"],"$",False,3.7,"11 Tai Tong Road","2476 8888","Daily 7-23",22.4440,114.0230,"Congee:35|Dim Sum:48|Roast Meat:62|Tea:10","family,casual"),
    ("Hung Fook Tong","鴻福堂","Yuen Long",["Dessert"],"$",False,3.8,"Kau Yuk Road","2475 8888","Daily 8-22",22.4435,114.0225,"Herbal Tea:20|Dessert:28|Soup:35","casual"),
    ("Tak Lee","得利","Yuen Long",["Hotpot","Chinese"],"$",False,3.6,"27 Castle Peak Road","2445 8888","Daily 12-00",22.4448,114.0235,"Hotpot:198|Beef:128|Veg:25","casual,family"),
    ("Chefs Table","Chef Table","Wong Tai Sin",["Fusion","Western"],"$$$",False,4.3,"28 Hong Keung Street","2323 8888","Mon-Sun 12-14:30 18-22:30",22.3420,114.1930,"Tasting Menu:688|Foie Gras:188|Duck Breast:288|Souffle:98","romantic,business"),
    ("Palace","皇府","Kwun Tong",["Chinese","Cantonese"],"$$",False,3.7,"88 Hung To Road","2755 8888","Mon-Sun 11:30-14:30 18-22:30",22.3120,114.2260,"Dim Sum Set:198|Roast Meat:88|Fish:168|Rice:68","family,casual"),
    ("Genki Sushi","元気寿司","Kwun Tong",["Japanese","Sushi"],"$$",False,3.9,"75 Wai Yip Street","2755 6688","Daily 11-23",22.3130,114.2270,"Salmon Sushi:32|Maki Roll:48|Tempura:65|Ramen:58|Tea:20","casual,family"),
    ("Mi Noodle","麵麵","Sham Shui Po",["Noodle","Chinese"],"$",False,3.8,"171 Lai Chi Kok Road","2788 8888","Daily 11-22",22.3305,114.1615,"Beef Noodles:42|Noodles:35|Dumpling:28|Tea:12","casual"),
    ("Sister Wah","姊妹餐廳","Sham Shui Po",["Noodle","Ramen"],"$",False,3.9,"116 Shum Shing Street","2708 8888","Daily 12-22",22.3310,114.1620,"Tonkotsu Ramen:68|Tantanmen:62|Gyoza:38|Beer:25","casual"),
]

class Command(BaseCommand):
    help = 'Seed 60 real HK restaurants'

    def handle(self, *args, **options):
        self.stdout.write('Seeding HK restaurants...')
        
        # Ensure reference data
        self._ensure_districts()
        self._ensure_cuisines()
        self._ensure_tags()
        self._ensure_users()
        
        dmap = {d.name_en: d for d in District.objects.all()}
        cmap = {c.name_en: c for c in Cuisine.objects.all()}
        tmap = {t.name_en: t for t in Tag.objects.all()}
        users = list(User.objects.filter(is_verified_diner=True))
        if not users:
            users = list(User.objects.all())
        
        created = 0
        for rdata in RESTAURANTS:
            (name_en, name_tc, dist_name, cuisines, price, featured,
             rating, address, phone, hours_str, lat, lng, menu_str, tag_str) = rdata
            
            slug_val = slugify(name_en)[:250]
            if Restaurant.objects.filter(slug=slug_val).exists():
                continue
            
            district = dmap.get(dist_name)
            if not district:
                continue
            
            # Parse hours
            hours = self._parse_hours(hours_str)
            
            try:
                r = Restaurant.objects.create(
                    name_en=name_en, name_tc=name_tc, slug=slug_val,
                    district=district, address_en=address, phone=phone,
                    price_range=price, opening_hours=hours,
                    avg_rating=rating, status='verified',
                    is_featured=featured, latitude=lat, longitude=lng,
                )
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Skip {name_en}: {e}'))
                continue
            
            # Cuisines
            for cn in cuisines:
                c = cmap.get(cn)
                if c:
                    r.cuisines.add(c)
            if not r.cuisines.exists():
                r.cuisines.add(random.choice(list(cmap.values())))
            
            # Tags
            for tn in tag_str.split(','):
                t = tmap.get(tn.strip())
                if t:
                    r.tags.add(t)
            
            # Menu items
            for item_str in menu_str.split('|'):
                item_str = item_str.strip()
                if ':' not in item_str:
                    continue
                iname, iprice_s = item_str.rsplit(':', 1)
                iname = iname.strip()
                try:
                    iprice = int(iprice_s.strip())
                except:
                    iprice = None
                cat = 'main'
                il = iname.lower()
                if any(w in il for w in ['soup','bisque','starter','appetizer','salad','bread','wings','fries','canape','bruschetta','terrine','parfait','platter']):
                    cat = 'appetizer'
                elif any(w in il for w in ['cake','tiramisu','pudding','souffle','ice','cream','tart','mochi','pancake','waffle','crepe','sago','jelly','fondant','brulee','flake','pie','cheesecake','mousse','parfait','toast','limefoam']):
                    cat = 'dessert'
                elif any(w in il for w in ['coffee','tea','juice','beer','wine','sangria','cocktail','milkshake','lassi','soda','cola','lemonade','espresso','latte','smoothie','shake']):
                    cat = 'drink'
                elif any(w in il for w in ['rice','noodles','noodle','pasta','spaghetti','bread','fries','rings','chips']):
                    if 'special' in il or iprice and iprice > 300:
                        cat = 'special'
                    else:
                        cat = 'side'
                elif iprice and iprice > 300:
                    cat = 'special'
                
                MenuItem.objects.get_or_create(
                    restaurant=r, name_en=iname[:200],
                    defaults={'price': iprice, 'category': cat, 'is_available': True}
                )
            
            # Reviews
            if users:
                titles = ['Great food!','Will come back','Average','Must try!','Hidden gem','Overpriced but good','Lovely atmosphere','Best in town','Disappointed','Worth it']
                bodies = [
                    'Amazing food and great service. Highly recommended.',
                    'The dishes were flavorful and well presented. Will come back!',
                    'Good food but a bit pricey for the portion size.',
                    'Lovely ambience and friendly staff. Food was decent.',
                    'One of the best meals in Hong Kong. Truly memorable.',
                    'The chef specials are incredible. Worth every dollar.',
                    'Great for date night. Romantic atmosphere.',
                    'Family friendly and good value for money.',
                    'Not as good as expected. Service was slow.',
                    'Excellent lamb and duck. Wine list is impressive.',
                ]
                n = random.randint(2, min(5, len(users)))
                for u in random.sample(users, n):
                    Review.objects.get_or_create(
                        restaurant=r, user=u,
                        defaults={
                            'rating': min(5, max(1, int(rating) + random.randint(-1, 1))),
                            'title': random.choice(titles),
                            'body': random.choice(bodies),
                            'meal_type': random.choice(['lunch','dinner','brunch','','supper']),
                            'is_published': True,
                            'is_verified': random.choice([True,False,False,False]),
                            'created_at': timezone.now() - timedelta(days=random.randint(1,120)),
                        }
                    )
            created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {created} restaurants'))
        self.stdout.write(self.style.SUCCESS(f'Total: {Restaurant.objects.count()} r/{Review.objects.count()} rev/{MenuItem.objects.count()} menu'))

    def _parse_hours(self, s):
        h = {}
        parts = s.replace('Daily ','Mon-Sun ').replace('  ',' ').split(' ')
        for p in parts:
            if '-' in p and ':' in p:
                # time range like 12-14:30
                for day in ['mon','tue','wed','thu','fri','sat','sun']:
                    if day not in h:
                        h[day] = p
            elif p.count('-') == 2 and ':' in p:
                # Mon-Sun style
                days, times = p.split(' ', 1) if ' ' in p else ('mon-sun', p)
                for day in ['mon','tue','wed','thu','fri','sat','sun']:
                    h[day] = times
        if not h:
            h = {'mon':'11:00-23:00','tue':'11:00-23:00','wed':'11:00-23:00','thu':'11:00-23:00','fri':'11:00-23:30','sat':'11:00-23:30','sun':'11:00-22:00'}
        return h

    def _ensure_districts(self):
        from apps.restaurants.models import District
        data = [
            ('Central','中環','HK',22.2819,114.1589),('Sheung Wan','上環','HK',22.2867,114.1474),
            ('Wan Chai','灣仔','HK',22.2783,114.1714),('Causeway Bay','銅鑼灣','HK',22.2800,114.1833),
            ('Admiralty','金鐘','HK',22.2786,114.1658),('Kennedy Town','堅尼地城','HK',22.2811,114.1289),
            ('Soho','蘇豪區','HK',22.2833,114.1533),('Aberdeen','香港仔','HK',22.2478,114.1572),
            ('Tsim Sha Tsui','尖沙咀','KLN',22.2988,114.1722),('Mong Kok','旺角','KLN',22.3192,114.1694),
            ('Yau Ma Tei','油麻地','KLN',22.3133,114.1706),('Jordan','佐敦','KLN',22.3050,114.1708),
            ('Prince Edward','太子','KLN',22.3247,114.1683),('Sham Shui Po','深水埗','KLN',22.3300,114.1614),
            ('Hung Hom','紅磡','KLN',22.3033,114.1828),('Kowloon City','九龍城','KLN',22.3303,114.1869),
            ('Wong Tai Sin','黃大仙','KLN',22.3425,114.1936),('Kwun Tong','觀塘','KLN',22.3125,114.2264),
            ('Tseung Kwan O','將軍澳','KLN',22.3075,114.2553),('Sha Tin','沙田','NT',22.3814,114.1881),
            ('Tai Wai','大圍','NT',22.3728,114.1786),('Tsuen Wan','荃灣','NT',22.3731,114.1175),
            ('Tuen Mun','屯門','NT',22.3914,113.9725),('Yuen Long','元朗','NT',22.4445,114.0228),
        ]
        for ne,nt,r,la,ln in data:
            District.objects.get_or_create(name_en=ne,defaults={'name_tc':nt,'region':r,'latitude':la,'longitude':ln})

    def _ensure_cuisines(self):
        data=[
            ('Chinese','中餐','ch'),('Cantonese','粵菜','ca'),('Dim Sum','點心','di'),
            ('Japanese','日本料理','ja'),('Sushi','壽司','su'),('Ramen','拉麵','ra'),
            ('Korean','韓國菜','ko'),('Thai','泰國菜','th'),('Vietnamese','越南菜','vi'),
            ('Western','西餐','we'),('Italian','意大利菜','it'),('French','法國菜','fr'),
            ('Steakhouse','牛排','st'),('Indian','印度菜','in'),('Noodle','粉麵','no'),
            ('Hotpot','火鍋','ho'),('Seafood','海鮮','se'),('Cafe','咖啡廳','cf'),
            ('Dessert','甜品','de'),('Bar','酒吧','ba'),('Cha Chaan Teng','茶餐廳','cc'),
            ('Fusion','Fusion','fu'),('Spanish','西班牙菜','sp'),('Peking','京菜','pe'),
            ('Sichuan','川菜','si'),('Malaysian','馬來西亞菜','ma'),('Taiwanese','台灣菜','tw'),
            ('Congee','粥品','cg'),('BBQ','燒烤','bb'),('Korean BBQ','韓式烤肉','kb'),
            ('Izakaya','居酒屋','iz'),('Shanghainese','上海菜','sh'),
        ]
        for ne,nt,ik in data:
            from apps.restaurants.models import Cuisine
            if not Cuisine.objects.filter(name_en=ne).exists():
                Cuisine.objects.create(name_en=ne,name_tc=nt,icon=ik)

    def _ensure_tags(self):
        data=[
            ('Vegetarian','素食','dietary'),('Vegan','純素','dietary'),('Halal','清真','dietary'),
            ('Gluten-Free','無麩質','dietary'),('Wifi','WiFi','amenity'),('Parking','停車','amenity'),
            ('Outdoor','戶外座位','amenity'),('Private Room','私人包房','amenity'),
            ('Pet Friendly','寵物友善','amenity'),('Wheelchair','無障礙','amenity'),
            ('Romantic','浪漫','atmosphere'),('Family','親子友善','atmosphere'),
            ('Business','商務','atmosphere'),('Casual','休閒','atmosphere'),
            ('Michelin','米芝蓮','atmosphere'),('No Smoking','禁煙','amenity'),
        ]
        for ne,nt,tt in data:
            from apps.restaurants.models import Tag
            if not Tag.objects.filter(name_en=ne).exists():
                Tag.objects.create(name_en=ne,name_tc=nt,tag_type=tt)

    def _ensure_users(self):
        from apps.accounts.models import User
        udata = [
            ('foodie_karl','karl@tf.hk','Karl'),('dimsum_queen','dq@tf.hk','Queen'),
            ('ramen_ken','ken@tf.hk','Ken'),('curry_jay','jay@tf.hk','Jay'),
            ('cafe_suki','suki@tf.hk','Suki'),('bbq_ben','ben@tf.hk','Ben'),
            ('noodle_nancy','nancy@tf.hk','Nancy'),('sushi_sam','sam@tf.hk','Sam'),
        ]
        for un,em,fn in udata:
            if not User.objects.filter(username=un).exists():
                u = User.objects.create_user(un,em,'testpass123')
                u.first_name = fn
                u.is_verified_diner = True
                u.save()

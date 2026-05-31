# TableFor - Quick Start Guide

## To run locally:

```bash
cd C:\Users\TonyChoi\Projects\tablefor
.\venv\Scripts\activate
python manage.py runserver 0.0.0.0:8002
```

Then open http://localhost:8002 in your browser.

## To deploy for free (3 options):

### Option 1: GitHub + Render (Recommended)
1. Go to github.com/new → create repo named `tablefor`
2. Go to render.com → New Web Service → connect the repo
3. Set build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py seed_data && python manage.py seed_restaurants`
4. Set start command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
5. Deploy!

### Option 2: PythonAnywhere (Free tier)
1. Go to pythonanywhere.com → create free account
2. Upload tablefor/ folder via Files tab
3. Open Bash console, run:
   ```bash
   cd tablefor
   pip3 install -r requirements.txt --user
   python3 manage.py migrate
   python3 manage.py seed_data
   python3 manage.py seed_restaurants
   ```
4. Create new Web app → Manual config → Python 3.11

### Option 3: ngrok (Instant public URL)
```bash
# In one terminal, run the dev server:
cd C:\Users\TonyChoi\Projects\tablefor
python manage.py runserver 8002

# In another terminal, install ngrok and run:
ngrok http 8002
```
This gives you a public URL like https://abc123.ngrok-free.app

## Admin Access
- URL: http://localhost:8002/admin/
- Username: admin
- Password: admin123

## Management Commands
```bash
python manage.py seed_data          # Districts, cuisines, tags, users
python manage.py seed_restaurants    # 58 HK restaurants with menus & reviews
```

## API Endpoints (future)
- GET /api/restaurants/ - List all restaurants
- GET /api/restaurants/{slug}/ - Restaurant detail
- GET /api/reviews/ - List reviews

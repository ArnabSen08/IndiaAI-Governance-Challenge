# Little Lemon Web Application

Django-based web application for Little Lemon restaurant featuring online booking, menu display, and customer management.

## 🚀 Features

- **Restaurant Homepage** - Elegant landing page with restaurant information
- **Menu Display** - Interactive menu with item details and pricing
- **Online Booking** - Table reservation system with date/time selection
- **Customer Management** - Customer profiles and booking history
- **RESTful API** - Backend API for mobile and third-party integrations
- **Admin Panel** - Django admin interface for restaurant management

## 🛠️ Technology Stack

- **Backend**: Django 4.2+, Django REST Framework
- **Database**: SQLite (development), MySQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with responsive design
- **API**: RESTful endpoints for all major operations

## 📁 Project Structure

```
webapp/
├── littlelemon/          # Django project settings
│   ├── settings.py      # Configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI configuration
├── restaurant/          # Main restaurant app
│   ├── models.py        # Database models
│   ├── views.py         # View logic
│   ├── urls.py          # App URLs
│   ├── forms.py         # Django forms
│   ├── serializers.py   # DRF serializers
│   ├── admin.py         # Admin configuration
│   ├── static/          # CSS, JS, images
│   └── templates/       # HTML templates
├── static/              # Collected static files
├── templates/           # Global templates
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or pipenv
- MySQL (for production)

### Installation

1. **Navigate to webapp directory**:
   ```bash
   cd webapp
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database** (edit `littlelemon/settings.py`):
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'LittleLemonDB',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

7. **Start development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Website: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - API: http://localhost:8000/api/

## 🔗 API Endpoints

### Menu API
- `GET /api/menu/` - List all menu items
- `GET /api/menu/{id}/` - Get specific menu item
- `POST /api/menu/` - Create menu item (admin)
- `PUT /api/menu/{id}/` - Update menu item (admin)
- `DELETE /api/menu/{id}/` - Delete menu item (admin)

### Booking API
- `GET /api/bookings/` - List bookings
- `POST /api/bookings/` - Create new booking
- `GET /api/bookings/{id}/` - Get specific booking
- `PUT /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Cancel booking

## 🎨 Frontend Features

- **Responsive Design** - Works on desktop, tablet, and mobile
- **Modern UI** - Clean, professional restaurant aesthetic
- **Interactive Forms** - User-friendly booking and contact forms
- **Image Gallery** - Showcase restaurant ambiance and food
- **Navigation** - Intuitive menu and page navigation

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

Run specific tests:
```bash
python manage.py test restaurant.tests.test_views
python manage.py test restaurant.tests.test_models
```

## 🚀 Deployment

### Production Settings
1. Set `DEBUG = False`
2. Configure production database
3. Set up static file serving
4. Configure allowed hosts
5. Set up environment variables

### Environment Variables
Create a `.env` file:
```
SECRET_KEY=your_secret_key
DEBUG=False
DATABASE_URL=mysql://user:password@host:port/database
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 📱 Mobile Responsiveness

The application is fully responsive and optimized for:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (320px - 767px)

## 🔒 Security Features

- CSRF protection
- SQL injection prevention
- XSS protection
- Secure authentication
- Input validation
- Admin access controls
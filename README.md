# Little Lemon Restaurant - Full Stack Project

A comprehensive restaurant management system built with Django, featuring database design, web application, and data analytics.

## 🚀 Project Overview

This project demonstrates a complete restaurant management solution for Little Lemon restaurant, including:

- **Database Design & Management**: MySQL database with stored procedures, views, and booking system
- **Web Application**: Django-based restaurant website with booking functionality
- **Data Analytics**: Tableau dashboards and Python data analysis
- **API Integration**: RESTful APIs for restaurant operations

## 📁 Project Structure

```
little-lemon-restaurant/
├── database/                 # Database design and SQL scripts
│   ├── schema/              # Database schema and models
│   ├── procedures/          # Stored procedures and functions
│   ├── analytics/           # Data analysis and visualizations
│   └── documentation/       # Database documentation
├── webapp/                  # Django web application
│   ├── littlelemon/        # Django project settings
│   ├── restaurant/         # Main restaurant app
│   ├── static/             # Static files (CSS, JS, images)
│   ├── templates/          # HTML templates
│   └── requirements.txt    # Python dependencies
├── docs/                   # Project documentation
└── README.md
```

## 🛠 Technologies Used

- **Backend**: Python, Django, Django REST Framework
- **Database**: MySQL, SQLite (development)
- **Frontend**: HTML5, CSS3, JavaScript
- **Analytics**: Python (Pandas, Jupyter), Tableau
- **Tools**: Git, Pipenv

## 📊 Features

### Database Features
- Complete restaurant database schema
- Booking management system
- Customer and order tracking
- Stored procedures for business logic
- Data analytics and reporting

### Web Application Features
- Restaurant homepage with menu display
- Online table booking system
- Customer management
- Responsive design
- RESTful API endpoints

### Analytics Features
- Sales and profit analysis
- Customer behavior insights
- Interactive Tableau dashboards
- Data visualization charts

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Node.js (for frontend dependencies)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ArnabSen08/little-lemon-restaurant.git
   cd little-lemon-restaurant
   ```

2. **Set up the database**
   ```bash
   cd database
   mysql -u root -p < schema/LittleLemonDB.sql
   ```

3. **Set up the web application**
   ```bash
   cd webapp
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

4. **Access the application**
   - Web App: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## 📈 Database Schema

The database includes the following main entities:
- **Customers**: Customer information and contact details
- **Bookings**: Table reservations and booking management
- **Menu**: Restaurant menu items and pricing
- **Orders**: Customer orders and order items
- **Staff**: Restaurant staff information

## 🔧 API Endpoints

- `GET /api/menu/` - Retrieve menu items
- `POST /api/bookings/` - Create new booking
- `GET /api/bookings/` - List all bookings
- `PUT /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Cancel booking

## 📊 Analytics & Reporting

The project includes comprehensive data analysis:
- Sales performance tracking
- Customer segmentation analysis
- Booking patterns and trends
- Revenue optimization insights

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Arnab Sen**
- GitHub: [@ArnabSen08](https://github.com/ArnabSen08)
- LinkedIn: [Arnab Sen](https://linkedin.com/in/arnab-sen)

## 🙏 Acknowledgments

- Meta Backend Developer Professional Certificate
- Little Lemon Restaurant (Fictional)
- Django Documentation
- MySQL Documentation
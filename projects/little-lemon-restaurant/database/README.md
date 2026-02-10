# Little Lemon Database

This directory contains the complete database design and implementation for the Little Lemon restaurant management system.

## 📁 Structure

- **SQL Scripts**: Database schema, stored procedures, and functions
- **Analytics**: Jupyter notebooks and data analysis files
- **Documentation**: Database diagrams and screenshots
- **Tableau Files**: Interactive dashboards and visualizations

## 🗄️ Database Schema

The database includes the following main tables:
- `Customers` - Customer information and contact details
- `Bookings` - Table reservations and booking management
- `MenuItems` - Restaurant menu items and pricing
- `Orders` - Customer orders and order details
- `Staff` - Restaurant staff information

## 📊 Key Features

### Stored Procedures
- `AddBooking` - Create new table reservations
- `AddValidBooking` - Validate and create bookings
- `UpdateBooking` - Modify existing reservations
- `CancelBooking` - Cancel table reservations
- `CheckBooking` - Verify booking availability

### Views
- `OrdersView` - Comprehensive order information
- Customer sales analysis
- Revenue and profit calculations

### Analytics
- Sales performance tracking
- Customer behavior analysis
- Revenue optimization insights
- Interactive Tableau dashboards

## 🚀 Setup Instructions

1. **Install MySQL 8.0+**
2. **Create Database**:
   ```sql
   CREATE DATABASE LittleLemonDB;
   USE LittleLemonDB;
   ```
3. **Run Schema Script**:
   ```bash
   mysql -u root -p LittleLemonDB < LittleLemonDB.sql
   ```
4. **Load Sample Data** (if available)
5. **Test Stored Procedures**

## 📈 Analytics Files

- `Little Lemon Booking System.ipynb` - Python data analysis
- `Little Lemon Tableau.twbx` - Tableau dashboard
- `Little Lemon Excel File.xlsx` - Data export and analysis
- Various chart images showing sales, profits, and customer insights
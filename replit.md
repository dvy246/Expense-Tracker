# Expense Tracker Pro 💰

## Overview
A modern, aesthetic expense tracking web application built with Streamlit and Python. Features a beautiful gradient UI, interactive visualizations using Plotly, and comprehensive expense management capabilities.

## Project Structure
```
├── app.py                  # Main Streamlit application (enhanced UI)
├── expense_tracker.py      # Core expense tracking logic (clean backend)
├── expenseclass.py        # Original expense class (legacy - not used)
├── expenses.csv           # Data storage (CSV format)
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── .gitignore             # Git ignore rules
```

## Features
- ✨ **Modern Aesthetic UI**: Gradient backgrounds, card-based layout, custom CSS styling
- 📊 **Interactive Dashboard**: Real-time metrics and visualizations
- 📈 **Advanced Analytics**: Spending trends, heatmaps, category breakdowns
- 🔍 **Smart Filtering**: Date ranges, categories, search functionality
- 📥 **Data Export**: Download expenses as CSV
- 📱 **Responsive Design**: Works on all screen sizes

## Technology Stack
- **Backend**: Python 3.11
- **Frontend**: Streamlit
- **Visualizations**: Plotly, Matplotlib
- **Data Processing**: Pandas
- **Styling**: Custom CSS with gradients and modern design

## Recent Changes (October 2025)
- Created new enhanced frontend with modern aesthetic design
- Implemented cleaner backend structure in `expense_tracker.py`
- Added Plotly for interactive visualizations
- Configured Streamlit for Replit environment (port 5000, all hosts allowed)
- Added comprehensive filtering and analytics features
- Improved code organization and structure

## User Preferences
- Clean, organized code structure
- Modern, aesthetic UI design
- Enhanced user experience

## Setup & Configuration
- Streamlit runs on port 5000 (0.0.0.0)
- CORS and XSRF protection disabled for Replit proxy
- CSV-based data persistence
- No database required

## Categories
The app supports 10 expense categories:
1. Food & Dining
2. Transportation
3. Shopping
4. Entertainment
5. Bills & Utilities
6. Health & Fitness
7. Travel
8. Education
9. Personal Care
10. Other

## Deployment
Configured for Replit Autoscale deployment with optimized settings for web applications.

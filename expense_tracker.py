from datetime import datetime
import pandas as pd
import csv
import os

class ExpenseTracker:
    """Enhanced expense tracking class with cleaner structure"""
    
    CATEGORIES = [
        'Food & Dining',
        'Transportation',
        'Shopping',
        'Entertainment',
        'Bills & Utilities',
        'Health & Fitness',
        'Travel',
        'Education',
        'Personal Care',
        'Other'
    ]
    
    def __init__(self, filepath='expenses.csv'):
        self.filepath = filepath
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        """Create expenses file if it doesn't exist"""
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Description', 'Category', 'Amount'])
    
    def add_expense(self, date, description, category, amount):
        """Add a new expense to the CSV file"""
        try:
            with open(self.filepath, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([date, description, category, amount])
            return True
        except Exception as e:
            print(f"Error adding expense: {e}")
            return False
    
    def get_expenses(self):
        """Load all expenses from CSV"""
        try:
            df = pd.read_csv(self.filepath)
            if df.empty:
                return pd.DataFrame(columns=['Date', 'Description', 'Category', 'Amount'])
            df['Date'] = pd.to_datetime(df['Date'])
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
            return df.dropna()
        except FileNotFoundError:
            return pd.DataFrame(columns=['Date', 'Description', 'Category', 'Amount'])
        except Exception as e:
            print(f"Error loading expenses: {e}")
            return pd.DataFrame(columns=['Date', 'Description', 'Category', 'Amount'])
    
    def get_total(self):
        """Get total expenses"""
        df = self.get_expenses()
        return df['Amount'].sum() if not df.empty else 0.0
    
    def get_category_totals(self):
        """Get expenses grouped by category"""
        df = self.get_expenses()
        if df.empty:
            return pd.Series(dtype=float)
        return df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    
    def get_monthly_totals(self):
        """Get expenses grouped by month"""
        df = self.get_expenses()
        if df.empty:
            return pd.Series(dtype=float)
        df['Month'] = df['Date'].dt.to_period('M')
        return df.groupby('Month')['Amount'].sum()
    
    def clear_all_expenses(self):
        """Clear all expenses from the file"""
        try:
            with open(self.filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Description', 'Category', 'Amount'])
            return True
        except Exception as e:
            print(f"Error clearing expenses: {e}")
            return False
    
    def delete_expense(self, index):
        """Delete an expense by index"""
        try:
            df = pd.read_csv(self.filepath)
            df = df.drop(index)
            df.to_csv(self.filepath, index=False)
            return True
        except Exception as e:
            print(f"Error deleting expense: {e}")
            return False

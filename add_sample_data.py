#!/usr/bin/env python3
"""
Script to add sample data to the Budget Prediction App database.
Run this script to populate the database with demo expenses and income data.
"""

from app import app, db, Category, Expense, Income, SavingsGoal, UserSettings
from datetime import date, timedelta
import random

def add_sample_data():
    """Add sample data to the database for demonstration purposes."""
    
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        
        print("Adding sample data to Budget Prediction App...")
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("Clearing existing data...")
        Expense.query.delete()
        Income.query.delete()
        SavingsGoal.query.delete()
        
        # Get categories
        categories = Category.query.all()
        if not categories:
            print("No categories found. Please run the main app first to create categories.")
            return
        
        # Create sample income data
        print("Adding sample income...")
        income_sources = [
            {"source": "Salary", "amount": 5000.00},
            {"source": "Freelance Work", "amount": 800.00},
            {"source": "Investment Returns", "amount": 200.00},
            {"source": "Side Business", "amount": 300.00}
        ]
        
        for income_data in income_sources:
            income = Income(
                amount=income_data["amount"],
                source=income_data["source"],
                date=date.today() - timedelta(days=random.randint(1, 10))
            )
            db.session.add(income)
        
        # Create sample expenses for the last 30 days
        print("Adding sample expenses...")
        
        # Sample expense data
        sample_expenses = [
            # Food expenses
            {"description": "Grocery shopping at Whole Foods", "amount": 120.50, "category": "Food"},
            {"description": "Dinner at restaurant", "amount": 45.80, "category": "Food"},
            {"description": "Coffee and snacks", "amount": 15.20, "category": "Food"},
            {"description": "Lunch with colleagues", "amount": 25.60, "category": "Food"},
            {"description": "Weekend brunch", "amount": 38.90, "category": "Food"},
            {"description": "Pizza delivery", "amount": 32.40, "category": "Food"},
            
            # Transportation expenses
            {"description": "Gas for car", "amount": 65.00, "category": "Transportation"},
            {"description": "Uber ride to airport", "amount": 28.50, "category": "Transportation"},
            {"description": "Public transport pass", "amount": 45.00, "category": "Transportation"},
            {"description": "Parking fee", "amount": 12.00, "category": "Transportation"},
            
            # Entertainment expenses
            {"description": "Movie tickets", "amount": 24.00, "category": "Entertainment"},
            {"description": "Concert tickets", "amount": 85.00, "category": "Entertainment"},
            {"description": "Netflix subscription", "amount": 15.99, "category": "Entertainment"},
            {"description": "Gaming purchase", "amount": 59.99, "category": "Entertainment"},
            
            # Clothes expenses
            {"description": "New jeans", "amount": 79.99, "category": "Clothes"},
            {"description": "Winter jacket", "amount": 149.99, "category": "Clothes"},
            {"description": "Sneakers", "amount": 89.99, "category": "Clothes"},
            
            # Utilities expenses
            {"description": "Electric bill", "amount": 125.50, "category": "Utilities"},
            {"description": "Internet bill", "amount": 69.99, "category": "Utilities"},
            {"description": "Phone bill", "amount": 45.00, "category": "Utilities"},
            
            # Healthcare expenses
            {"description": "Doctor visit", "amount": 150.00, "category": "Healthcare"},
            {"description": "Prescription medication", "amount": 35.80, "category": "Healthcare"},
            
            # Education expenses
            {"description": "Online course", "amount": 199.99, "category": "Education"},
            {"description": "Books", "amount": 45.60, "category": "Education"},
            
            # Extra expenses
            {"description": "Gift for friend", "amount": 55.00, "category": "Extra"},
            {"description": "Charity donation", "amount": 100.00, "category": "Extra"},
            {"description": "Home repair", "amount": 85.50, "category": "Extra"}
        ]
        
        # Add expenses with random dates in the last 30 days
        for expense_data in sample_expenses:
            # Find category
            category = Category.query.filter_by(name=expense_data["category"]).first()
            if not category:
                continue
            
            # Create expense
            expense_date = date.today() - timedelta(days=random.randint(1, 30))
            
            # Randomly make some expenses split
            is_split = random.choice([True, False])
            total_people = random.randint(2, 4) if is_split else 1
            split_amount = expense_data["amount"] / total_people if is_split else expense_data["amount"]
            
            expense = Expense(
                amount=expense_data["amount"],
                description=expense_data["description"],
                category_id=category.id,
                date=expense_date,
                is_split=is_split,
                total_people=total_people,
                split_amount=split_amount
            )
            db.session.add(expense)
        
        # Create a sample savings goal
        print("Adding sample savings goal...")
        savings_goal = SavingsGoal(
            target_amount=1000.00,
            current_amount=450.00,  # Partially achieved
            month=date.today().month,
            year=date.today().year
        )
        db.session.add(savings_goal)
        
        # Commit all changes
        db.session.commit()
        
        print("Sample data added successfully!")
        print(f"Added {len(sample_expenses)} expenses")
        print(f"Added {len(income_sources)} income entries")
        print("Added 1 savings goal")
        print("\nYou can now run the Flask app and see the sample data in action!")

if __name__ == "__main__":
    add_sample_data()

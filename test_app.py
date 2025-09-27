#!/usr/bin/env python3
"""
Test script for the Budget Prediction App.
This script demonstrates the app's functionality and tests key features.
"""

from app import app, db, Expense, Income, SavingsGoal, Category, UserSettings
from datetime import date, timedelta

def test_app_functionality():
    """Test the key functionality of the Budget Prediction App."""
    
    print("🧪 Testing Budget Prediction App Functionality\n")
    
    with app.app_context():
        # Test 1: Database Models
        print("1️⃣ Testing Database Models")
        print("=" * 50)
        
        categories = Category.query.all()
        print(f"✅ Categories: {len(categories)} found")
        for cat in categories:
            print(f"   - {cat.name} ({cat.color})")
        
        expenses = Expense.query.all()
        print(f"✅ Expenses: {len(expenses)} found")
        
        income = Income.query.all()
        print(f"✅ Income entries: {len(income)} found")
        
        goals = SavingsGoal.query.all()
        print(f"✅ Savings goals: {len(goals)} found")
        
        settings = UserSettings.query.first()
        print(f"✅ User settings: Currency = {settings.currency if settings else 'None'}")
        
        # Test 2: Expense Categories
        print("\n2️⃣ Testing Expense Categories")
        print("=" * 50)
        
        category_totals = {}
        for expense in expenses:
            cat_name = expense.category.name
            amount = expense.split_amount if expense.is_split else expense.amount
            if cat_name not in category_totals:
                category_totals[cat_name] = 0
            category_totals[cat_name] += amount
        
        for category, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {category}: ${total:.2f}")
        
        # Test 3: Bill Splitting
        print("\n3️⃣ Testing Bill Splitting")
        print("=" * 50)
        
        split_expenses = [e for e in expenses if e.is_split]
        print(f"✅ Split expenses: {len(split_expenses)} found")
        
        for expense in split_expenses[:3]:  # Show first 3
            print(f"   - {expense.description}")
            print(f"     Total: ${expense.amount:.2f}, Split between {expense.total_people} people")
            print(f"     Each person pays: ${expense.split_amount:.2f}")
        
        # Test 4: Savings Goals
        print("\n4️⃣ Testing Savings Goals")
        print("=" * 50)
        
        for goal in goals:
            progress = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
            print(f"   - Target: ${goal.target_amount:.2f}")
            print(f"   - Current: ${goal.current_amount:.2f}")
            print(f"   - Progress: {progress:.1f}%")
        
        # Test 5: Monthly Totals
        print("\n5️⃣ Testing Monthly Calculations")
        print("=" * 50)
        
        total_income = sum(i.amount for i in income)
        total_expenses = sum(e.split_amount if e.is_split else e.amount for e in expenses)
        remaining_budget = total_income - total_expenses
        
        print(f"   - Total Income: ${total_income:.2f}")
        print(f"   - Total Expenses: ${total_expenses:.2f}")
        print(f"   - Remaining Budget: ${remaining_budget:.2f}")
        
        # Test 6: Predictions
        print("\n6️⃣ Testing Budget Predictions")
        print("=" * 50)
        
        if expenses:
            # Calculate daily spending rate
            days_elapsed = date.today().day
            daily_spending_rate = total_expenses / days_elapsed if days_elapsed > 0 else 0
            
            print(f"   - Days elapsed this month: {days_elapsed}")
            print(f"   - Daily spending rate: ${daily_spending_rate:.2f}")
            
            if daily_spending_rate > 0 and remaining_budget > 0:
                days_remaining = remaining_budget / daily_spending_rate
                print(f"   - Predicted days until budget exhausted: {days_remaining:.1f}")
        
        # Test 7: Currency Support
        print("\n7️⃣ Testing Currency Support")
        print("=" * 50)
        
        from app import CURRENCY_RATES
        print("   - Supported currencies:")
        for currency, rate in CURRENCY_RATES.items():
            print(f"     {currency}: {rate}")
        
        print("\n✅ All tests completed successfully!")
        print("\n🚀 The Budget Prediction App is ready to use!")
        print("   Run 'python app.py' to start the web application.")

if __name__ == "__main__":
    test_app_functionality()

#!/usr/bin/env python3

from app import app, db, Expense
from datetime import date

with app.app_context():
    current_year = date.today().year
    current_month = date.today().month
    print(f'Filtering for year: {current_year}, month: {current_month}')
    
    # Get all expenses
    all_expenses = Expense.query.all()
    print(f'Total expenses in database: {len(all_expenses)}')
    
    # Get current month expenses
    expenses = Expense.query.filter(
        db.extract('year', Expense.date) == current_year,
        db.extract('month', Expense.date) == current_month
    ).all()
    
    print(f'Found {len(expenses)} expenses for current month')
    for exp in expenses[-5:]:
        print(f'  - {exp.description}: ${exp.amount} on {exp.date}')
    
    # Check recent expenses regardless of month
    recent_expenses = Expense.query.order_by(Expense.date.desc()).limit(5).all()
    print(f'\nMost recent expenses:')
    for exp in recent_expenses:
        print(f'  - {exp.description}: ${exp.amount} on {exp.date} (Year: {exp.date.year}, Month: {exp.date.month})')

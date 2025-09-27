#!/usr/bin/env python3

from app import app, db, Expense, get_monthly_data, convert_currency, get_current_currency
from datetime import date

with app.app_context():
    expenses, income = get_monthly_data()
    current_currency = get_current_currency()
    
    # Calculate total in USD first
    total_expenses_usd = sum(e.split_amount if e.is_split else e.amount for e in expenses)
    print(f'Total expenses in USD: {total_expenses_usd:.2f}')
    
    # Then convert
    total_expenses_converted = convert_currency(total_expenses_usd, 'USD', current_currency)
    print(f'Total expenses in {current_currency}: {total_expenses_converted:.2f}')
    
    # Show recent expenses
    recent = expenses[-3:]
    print(f'\nRecent expenses:')
    for exp in recent:
        converted_amount = convert_currency(exp.amount, 'USD', current_currency)
        print(f'  - {exp.description}: ${exp.amount} USD = {converted_amount:.2f} {current_currency}')
    
    # Check if new expenses are included
    print(f'\nTotal number of expenses this month: {len(expenses)}')
    print(f'Last 5 expenses:')
    for exp in expenses[-5:]:
        print(f'  - {exp.description}: ${exp.amount} on {exp.date}')

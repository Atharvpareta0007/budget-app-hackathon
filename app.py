from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, date
import plotly
import plotly.graph_objs as go
import plotly.utils
import json
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Currency conversion rates (simplified - in real app, use API)
CURRENCY_RATES = {
    'USD': 1.0,
    'EUR': 0.85,
    'INR': 83.0,
    'GBP': 0.73,
    'CAD': 1.35,
    'AUD': 1.50
}

# Database Models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(7), nullable=False, default='#28a745')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    is_split = db.Column(db.Boolean, default=False)
    total_people = db.Column(db.Integer, default=1)
    split_amount = db.Column(db.Float, default=0.0)
    
    category = db.relationship('Category', backref=db.backref('expenses', lazy=True))
    
    def __repr__(self):
        return f'<Expense {self.description}: ${self.amount}>'

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    
    def __repr__(self):
        return f'<Income {self.source}: ${self.amount}>'

class SavingsGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.Date, nullable=False, default=date.today)
    
    def __repr__(self):
        return f'<SavingsGoal {self.month}/{self.year}: ${self.current_amount}/${self.target_amount}>'

class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), default='USD')
    
    def __repr__(self):
        return f'<UserSettings currency: {self.currency}>'

# Helper Functions
def get_current_currency():
    settings = UserSettings.query.first()
    return settings.currency if settings else 'USD'

def get_currency_symbol(currency):
    symbols = {'USD': '$', 'EUR': '€', 'INR': '₹', 'GBP': '£', 'CAD': 'C$', 'AUD': 'A$'}
    return symbols.get(currency, '$')

# Make function available in templates (will be updated after function definitions)

def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
    return amount * CURRENCY_RATES[to_currency] / CURRENCY_RATES[from_currency]

def format_currency(amount, currency='USD'):
    symbols = {'USD': '$', 'EUR': '€', 'INR': '₹', 'GBP': '£', 'CAD': 'C$', 'AUD': 'A$'}
    symbol = symbols.get(currency, '$')
    return f"{symbol}{amount:,.2f}"

# Make functions available in templates
app.jinja_env.globals.update(
    get_currency_symbol=get_currency_symbol,
    convert_currency=convert_currency
)

def get_monthly_data(year=None, month=None):
    if not year:
        year = date.today().year
    if not month:
        month = date.today().month
    
    expenses = Expense.query.filter(
        db.extract('year', Expense.date) == year,
        db.extract('month', Expense.date) == month
    ).all()
    
    income = Income.query.filter(
        db.extract('year', Income.date) == year,
        db.extract('month', Income.date) == month
    ).all()
    
    return expenses, income

def calculate_savings_recommendation():
    current_date = date.today()
    days_in_month = (date(current_date.year, current_date.month % 12 + 1, 1) - 
                    date(current_date.year, current_date.month, 1)).days
    
    expenses, income = get_monthly_data()
    total_income = sum(i.amount for i in income)
    total_expenses = sum(e.split_amount if e.is_split else e.amount for e in expenses)
    
    savings_goal = SavingsGoal.query.filter_by(
        month=current_date.month, 
        year=current_date.year
    ).first()
    
    if not savings_goal:
        return 0, 0, 0
    
    remaining_days = days_in_month - current_date.day + 1
    remaining_budget = total_income - total_expenses
    target_savings = savings_goal.target_amount - savings_goal.current_amount
    
    daily_save = target_savings / remaining_days if remaining_days > 0 else 0
    
    return daily_save, remaining_budget, target_savings

def predict_overspend():
    current_date = date.today()
    expenses, income = get_monthly_data()
    
    total_income = sum(i.amount for i in income)
    total_expenses = sum(e.split_amount if e.is_split else e.amount for e in expenses)
    
    if total_expenses == 0:
        return None, None
    
    # Calculate daily spending rate
    days_elapsed = current_date.day
    daily_spending_rate = total_expenses / days_elapsed if days_elapsed > 0 else 0
    
    # Predict when budget will be exhausted
    remaining_budget = total_income - total_expenses
    if daily_spending_rate > 0 and remaining_budget > 0:
        days_remaining = remaining_budget / daily_spending_rate
        predicted_date = current_date + relativedelta(days=int(days_remaining))
        return predicted_date, daily_spending_rate
    
    return None, daily_spending_rate

# API Routes for iOS App
@app.route('/api/categories')
def api_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'color': cat.color
    } for cat in categories])

@app.route('/api/expenses', methods=['GET', 'POST'])
def api_expenses():
    if request.method == 'GET':
        expenses = Expense.query.all()
        return jsonify([{
            'id': exp.id,
            'amount': exp.amount,
            'description': exp.description,
            'category_id': exp.category_id,
            'date': exp.date.isoformat(),
            'is_split': exp.is_split,
            'total_people': exp.total_people,
            'split_amount': exp.split_amount,
            'category': {
                'id': exp.category.id,
                'name': exp.category.name,
                'color': exp.category.color
            } if exp.category else None
        } for exp in expenses])
    
    elif request.method == 'POST':
        data = request.get_json()
        expense = Expense(
            amount=data['amount'],
            description=data['description'],
            category_id=data['category'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            is_split=data.get('is_split', False),
            total_people=data.get('total_people', 1),
            split_amount=data['amount'] / data.get('total_people', 1) if data.get('is_split', False) else data['amount']
        )
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({
            'id': expense.id,
            'amount': expense.amount,
            'description': expense.description,
            'category_id': expense.category_id,
            'date': expense.date.isoformat(),
            'is_split': expense.is_split,
            'total_people': expense.total_people,
            'split_amount': expense.split_amount
        })

@app.route('/api/income')
def api_income():
    income = Income.query.all()
    return jsonify([{
        'id': inc.id,
        'amount': inc.amount,
        'source': inc.source,
        'date': inc.date.isoformat()
    } for inc in income])

@app.route('/api/savings-goal', methods=['GET', 'POST'])
def api_savings_goal():
    if request.method == 'GET':
        current_month = date.today().month
        current_year = date.today().year
        goal = SavingsGoal.query.filter_by(month=current_month, year=current_year).first()
        
        if goal:
            return jsonify({
                'id': goal.id,
                'target_amount': goal.target_amount,
                'current_amount': goal.current_amount,
                'month': goal.month,
                'year': goal.year,
                'created_date': goal.created_date.isoformat()
            })
        return jsonify(None)
    
    elif request.method == 'POST':
        data = request.get_json()
        current_month = date.today().month
        current_year = date.today().year
        
        goal = SavingsGoal.query.filter_by(month=current_month, year=current_year).first()
        if goal:
            goal.target_amount = data['target_amount']
        else:
            goal = SavingsGoal(
                target_amount=data['target_amount'],
                month=current_month,
                year=current_year
            )
            db.session.add(goal)
        
        db.session.commit()
        return jsonify({
            'id': goal.id,
            'target_amount': goal.target_amount,
            'current_amount': goal.current_amount,
            'month': goal.month,
            'year': goal.year,
            'created_date': goal.created_date.isoformat()
        })

@app.route('/api/settings', methods=['GET', 'POST'])
def api_settings():
    if request.method == 'GET':
        settings = UserSettings.query.first()
        if settings:
            return jsonify({
                'id': settings.id,
                'currency': settings.currency
            })
        return jsonify({'id': 1, 'currency': 'USD'})
    
    elif request.method == 'POST':
        data = request.get_json()
        settings = UserSettings.query.first()
        if settings:
            settings.currency = data['currency']
        else:
            settings = UserSettings(currency=data['currency'])
            db.session.add(settings)
        
        db.session.commit()
        return jsonify({
            'id': settings.id,
            'currency': settings.currency
        })

# Web Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    current_currency = get_current_currency()
    expenses, income = get_monthly_data()
    
    total_income = sum(i.amount for i in income)
    total_expenses = sum(e.split_amount if e.is_split else e.amount for e in expenses)
    
    # Convert to current currency
    total_income = convert_currency(total_income, 'USD', current_currency)
    total_expenses = convert_currency(total_expenses, 'USD', current_currency)
    
    daily_save, remaining_budget, target_savings = calculate_savings_recommendation()
    daily_save = convert_currency(daily_save, 'USD', current_currency)
    remaining_budget = convert_currency(remaining_budget, 'USD', current_currency)
    target_savings = convert_currency(target_savings, 'USD', current_currency)
    
    predicted_date, spending_rate = predict_overspend()
    
    # Category breakdown
    category_data = {}
    for expense in expenses:
        category_name = expense.category.name
        amount = expense.split_amount if expense.is_split else expense.amount
        amount = convert_currency(amount, 'USD', current_currency)
        
        if category_name not in category_data:
            category_data[category_name] = 0
        category_data[category_name] += amount
    
    # Create charts
    pie_chart = create_pie_chart(category_data, current_currency)
    bar_chart = create_bar_chart(category_data, current_currency)
    
    savings_goal = SavingsGoal.query.filter_by(
        month=date.today().month, 
        year=date.today().year
    ).first()
    
    savings_progress = 0
    if savings_goal:
        current_savings = convert_currency(savings_goal.current_amount, 'USD', current_currency)
        target_amount = convert_currency(savings_goal.target_amount, 'USD', current_currency)
        savings_progress = (current_savings / target_amount * 100) if target_amount > 0 else 0
    
    return render_template('dashboard.html',
                         total_income=total_income,
                         total_expenses=total_expenses,
                         remaining_budget=remaining_budget,
                         daily_save=daily_save,
                         target_savings=target_savings,
                         predicted_date=predicted_date,
                         spending_rate=spending_rate,
                         category_data=category_data,
                         pie_chart=pie_chart,
                         bar_chart=bar_chart,
                         savings_progress=savings_progress,
                         current_currency=current_currency)

@app.route('/add-expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        description = request.form['description']
        category_id = int(request.form['category'])
        expense_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        is_split = 'is_split' in request.form
        total_people = int(request.form.get('total_people', 1))
        
        split_amount = amount / total_people if is_split else amount
        
        expense = Expense(
            amount=amount,
            description=description,
            category_id=category_id,
            date=expense_date,
            is_split=is_split,
            total_people=total_people,
            split_amount=split_amount
        )
        
        db.session.add(expense)
        db.session.commit()
        
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    categories = Category.query.all()
    
    # Get recent expenses for the history table
    recent_expenses = Expense.query.order_by(Expense.date.desc()).limit(10).all()
    current_currency = get_current_currency()
    
    return render_template('add_expense.html', 
                         categories=categories, 
                         recent_expenses=recent_expenses,
                         current_currency=current_currency)

@app.route('/split-bill')
def split_bill():
    return render_template('split_bill.html')

@app.route('/savings-goal', methods=['GET', 'POST'])
def savings_goal():
    if request.method == 'POST':
        target_amount = float(request.form['target_amount'])
        current_month = date.today().month
        current_year = date.today().year
        
        # Check if goal already exists for this month
        existing_goal = SavingsGoal.query.filter_by(
            month=current_month, 
            year=current_year
        ).first()
        
        if existing_goal:
            existing_goal.target_amount = target_amount
        else:
            goal = SavingsGoal(
                target_amount=target_amount,
                month=current_month,
                year=current_year
            )
            db.session.add(goal)
        
        db.session.commit()
        flash('Savings goal updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    current_goal = SavingsGoal.query.filter_by(
        month=date.today().month, 
        year=date.today().year
    ).first()
    
    current_currency = get_current_currency()
    target_amount = 0
    if current_goal:
        target_amount = convert_currency(current_goal.target_amount, 'USD', current_currency)
    
    return render_template('savings_goal.html', 
                         current_goal=current_goal, 
                         target_amount=target_amount,
                         current_currency=current_currency)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        currency = request.form['currency']
        
        settings = UserSettings.query.first()
        if settings:
            settings.currency = currency
        else:
            settings = UserSettings(currency=currency)
            db.session.add(settings)
        
        db.session.commit()
        flash('Currency updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    current_currency = get_current_currency()
    return render_template('settings.html', 
                         current_currency=current_currency,
                         currencies=CURRENCY_RATES.keys())

# Chart creation functions
def create_pie_chart(category_data, currency):
    if not category_data:
        return None
    
    labels = list(category_data.keys())
    values = list(category_data.values())
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(
        title="Expenses by Category",
        height=400,
        showlegend=True
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_bar_chart(category_data, currency):
    if not category_data:
        return None
    
    labels = list(category_data.keys())
    values = list(category_data.values())
    
    fig = go.Figure(data=[go.Bar(x=labels, y=values)])
    fig.update_layout(
        title="Expenses by Category",
        xaxis_title="Categories",
        yaxis_title=f"Amount ({currency})",
        height=400
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Initialize database with sample data
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default categories if they don't exist
        categories = [
            ('Food', '#28a745'),
            ('Clothes', '#007bff'),
            ('Entertainment', '#6f42c1'),
            ('Transportation', '#fd7e14'),
            ('Healthcare', '#dc3545'),
            ('Education', '#20c997'),
            ('Utilities', '#6c757d'),
            ('Extra', '#ffc107')
        ]
        
        for name, color in categories:
            if not Category.query.filter_by(name=name).first():
                category = Category(name=name, color=color)
                db.session.add(category)
        
        # Create default user settings
        if not UserSettings.query.first():
            settings = UserSettings(currency='USD')
            db.session.add(settings)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=8080, debug=True)

# Budget Prediction App 💰

A modern, responsive budget tracking and prediction application built with Python Flask. Track your income and expenses, split bills with friends, set savings goals, and get intelligent predictions about your spending patterns.

## Features 🌟

### Core Features
- **Expense Tracking**: Track income and expenses with categories (Food, Clothes, Entertainment, etc.)
- **Bill Splitting**: Split expenses between friends with automatic calculations
- **Interactive Charts**: Visualize expenses using Pie Charts and Bar Graphs with Plotly.js
- **Savings Goal Tracker**: Set monthly savings targets and monitor progress
- **Predictive Budgeting**: Forecast when you'll run out of budget based on spending rate
- **Daily Savings Recommendations**: Get daily save recommendations to meet your goals
- **Currency Support**: Switch between multiple currencies (USD, EUR, INR, GBP, CAD, AUD)

### Design & UI
- **Green Financial Theme**: Clean, modern UI with financial-themed colors
- **Responsive Design**: Works perfectly on mobile, tablet, and desktop
- **Bootstrap 5**: Modern, accessible interface components
- **Font Awesome Icons**: Beautiful financial-themed icons throughout
- **Interactive Elements**: Smooth animations and hover effects

## Technology Stack 🛠️

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Charts**: Plotly.js for interactive visualizations
- **Icons**: Font Awesome
- **Styling**: Custom CSS with green financial theme

## Installation & Setup 🚀

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download
```bash
# If you have git, clone the repository
git clone <repository-url>
cd budget-prediction-app

# Or download and extract the ZIP file
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Initialize Database
```bash
python app.py
```
This will create the database and initialize with default categories.

### Step 4: Add Sample Data (Optional)
```bash
python add_sample_data.py
```
This adds sample expenses, income, and savings goals for demonstration.

### Step 5: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage Guide 📖

### Dashboard
- View your financial overview with key statistics
- See interactive charts of your spending by category
- Get budget predictions and alerts
- Monitor your savings goal progress

### Adding Expenses
1. Click "Add Expense" in the navigation
2. Fill in amount, description, category, and date
3. Optionally split the bill with friends
4. Save to track your spending

### Bill Splitting
1. Navigate to "Split Bill"
2. Enter the total bill amount
3. Specify number of people and tip percentage
4. Get automatic calculations for each person's share
5. Save as an expense if needed

### Savings Goals
1. Go to "Savings Goal" page
2. Set your monthly savings target
3. Monitor progress with visual progress bars
4. Get daily save recommendations

### Settings
- Change your preferred currency
- View supported currencies and exchange rates
- Access app information and features

## Project Structure 📁

```
budget-prediction-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── add_sample_data.py     # Script to add demo data
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── dashboard.html    # Main dashboard
│   ├── add_expense.html  # Add expense form
│   ├── split_bill.html   # Bill splitter calculator
│   ├── savings_goal.html # Savings goal management
│   └── settings.html     # Application settings
└── budget_app.db         # SQLite database (created automatically)
```

## Database Models 🗄️

- **Category**: Expense categories with colors
- **Expense**: Individual expenses with split functionality
- **Income**: Income sources and amounts
- **SavingsGoal**: Monthly savings targets and progress
- **UserSettings**: User preferences (currency, etc.)

## Key Features Explained 🔍

### Predictive Budgeting
The app analyzes your spending patterns and predicts when you might run out of budget based on:
- Current spending rate
- Remaining budget
- Days left in the month

### Currency Conversion
Supports multiple currencies with automatic conversion:
- USD (US Dollar) - $1.00
- EUR (Euro) - €0.85
- INR (Indian Rupee) - ₹83.00
- GBP (British Pound) - £0.73
- CAD (Canadian Dollar) - C$1.35
- AUD (Australian Dollar) - A$1.50

### Interactive Charts
- **Pie Chart**: Shows expense distribution by category
- **Bar Chart**: Displays category-wise spending amounts
- Built with Plotly.js for interactivity and responsiveness

## Customization 🎨

### Adding New Categories
Categories are automatically created when the app starts. To add custom categories:
1. Edit the `categories` list in `app.py`
2. Restart the application

### Changing the Theme
The app uses CSS custom properties for easy theming:
```css
:root {
    --primary-green: #28a745;
    --secondary-green: #20c997;
    --dark-green: #1e7e34;
    --light-green: #d4edda;
    --success-green: #155724;
}
```

### Adding New Currencies
1. Add currency to `CURRENCY_RATES` in `app.py`
2. Add currency symbol to templates
3. Update the settings dropdown

## API Endpoints 📡

- `GET /` - Redirects to dashboard
- `GET /dashboard` - Main dashboard with charts and statistics
- `GET/POST /add-expense` - Add new expense form
- `GET /split-bill` - Bill splitter calculator
- `GET/POST /savings-goal` - Savings goal management
- `GET/POST /settings` - Application settings

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License 📄

This project is open source and available under the MIT License.

## Support 💬

If you encounter any issues or have questions:
1. Check the README for common solutions
2. Review the code comments
3. Create an issue with detailed information

## Future Enhancements 🚀

Potential features for future versions:
- User authentication and multi-user support
- Data export/import functionality
- Advanced analytics and reports
- Mobile app version
- Integration with banking APIs
- Recurring expense tracking
- Budget categories and limits
- Expense photo attachments

---

**Built with ❤️ using Flask, Bootstrap, and Plotly.js**

# My Budget
#### Video Demo:  <URL HERE>
#### Description:

My Budget is a comprehensive web application designed to empower users to take control of their personal finances. Built with Python, Flask, and SQL, this tool moves beyond simple expense tracking to provide a full suite of features for budgeting, financial planning, and data visualization. In a world where financial literacy is paramount, My Budget offers a simple yet powerful platform for users to understand their spending habits, plan for the future, and achieve their financial goals.

The application is born from the foundational concepts learned in CS50, particularly inspired by the CS50 Finance problem set. It takes the core structure of a user-based web application and expands it into a feature-rich, practical tool for everyday life. Users can register for a secure account, log their income and expenses with custom categories, set monthly budgets to curb spending, visualize their financial data through interactive charts, and even automate recurring transactions. The goal of My Budget is not just to be a final project, but a durable, useful piece of software that can genuinely help users manage their money more effectively.

Features
My Budget is packed with features designed to provide a complete overview of a user's financial health:

Secure User Authentication:

Users can register for a new account with a unique username and a secure, hashed password.

Existing users can log in and out, with all their financial data kept private and secure through a session-based system.

Comprehensive Dashboard:

The main dashboard provides an at-a-glance summary of the current month's finances, including total income, total expenses, and the current balance.

It also displays a list of the most recent transactions for a quick review.

Transaction Management:

An intuitive form allows users to add new transactions, classifying them as either 'Income' or 'Expense'.

Each transaction can be assigned to a category and include an optional description.

Users can easily delete any transaction from their history, correcting mistakes with a single click.

Category Management:

The application comes with a set of default categories (e.g., Food, Housing, Salary).

Users have the power to create their own custom categories to perfectly match their lifestyle and spending habits.

Custom categories can be deleted at any time.

Monthly Budgeting System:

The core of proactive financial planning. Users can set monthly spending limits for any expense category.

The dashboard features dynamic progress bars for each budget, showing how much has been spent versus how much was budgeted.

The progress bars change color (blue, yellow, red) as the user approaches their limit, providing immediate visual feedback.

Visual Reports:

A dedicated reports page displays an interactive pie chart visualizing the distribution of expenses across different categories for the current month.

This feature, powered by Chart.js, helps users instantly identify where their money is going.

Transaction History with Filtering:

A detailed history page lists all past transactions in reverse chronological order.

Users can filter this history by month and/or category to analyze their spending patterns over time.

Recurring Transactions:

To automate financial tracking, users can set up recurring transactions (e.g., monthly salary, rent, or subscriptions).

The application intelligently checks and adds these transactions automatically once per month, simulating a cron job and ensuring the user's financial records are always up-to-date with minimal effort.

Technologies Used
Backend: Python, Flask

Database: SQLite

Frontend: HTML, CSS, JavaScript

Frameworks/Libraries: Bootstrap 5 for styling, Chart.js for data visualization, Jinja for templating.

File Structure & Purpose
app.py: The heart of the application. This file contains all the Flask routes and the core backend logic. It handles user authentication, database queries, calculations for the dashboard and reports, and serves all the HTML templates. It also includes the logic for the simulated automation of recurring transactions.

helpers.py: A module containing helper functions used throughout the application, following the design pattern from CS50 Finance. This includes the apology function for rendering error pages, the login_required decorator to protect routes, and a custom brl filter to format currency values into the Brazilian Real format.

schema.sql: The blueprint for the database. This file contains all the CREATE TABLE statements for users, transactions, categories, budgets, and recurring_transactions. It also includes INSERT statements to populate the database with default categories upon creation.

requirements.txt: Lists the Python dependencies required to run the application (Flask, Flask-Session, cs50).

templates/: This directory contains all the HTML files that are rendered to the user.

layout.html: The main template file that provides the consistent structure (navbar, footer) for all other pages.

index.html: The user's main dashboard, displaying financial summaries and budget progress bars.

login.html, register.html, apology.html: Standard pages for user authentication and error handling.

add.html: The form for adding a new transaction.

history.html: The page displaying all transactions, including the filtering form.

categories.html: The interface for users to view, add, and delete their custom categories.

reports.html: The page that contains the <canvas> element and JavaScript needed to render the expense pie chart.

budget.html: The interface for setting and viewing monthly budgets.

recurring.html: The interface for managing recurring transaction rules.

static/: Contains static files like custom CSS.

styles.css: Custom CSS rules to personalize the application's appearance, such as the styling for the chart container and the navigation bar.

Design Choices
The foundation of this project was heavily inspired by the CS50 Finance problem set. I chose to build upon its structure because it provided a robust and secure foundation for user authentication (register, login, logout) and a clear pattern for organizing a Flask application. This allowed me to focus my efforts on developing the core budgeting features that make "My Budget" unique.

SQLite was chosen as the database for its simplicity and serverless nature. For a personal finance application where data integrity is important but the scale is limited to a single user's data at a time, SQLite is a perfect fit. It avoids the complexity of setting up a larger database server while still providing the full power of SQL.

For the frontend, I relied on the Bootstrap 5 framework to achieve a clean, modern, and mobile-responsive design quickly. This allowed me to spend more time on the backend logic rather than on writing CSS from scratch. The visual components, like the progress bars and styled tables, are all powered by Bootstrap, ensuring a consistent user experience.

The most significant design choice was the implementation of the recurring transactions feature. Since a traditional server-side cron job (a time-based job scheduler) is not available in the development environment, I designed a simulated automation system. A check is performed every time the user loads their main dashboard. The system checks if the current month is different from the last_added month for each recurring rule. If it is, the transaction is added, and the last_added field is updated. This design ensures that recurring transactions are added reliably and only once per month, providing the desired automation within the constraints of the environment. This was a challenging but rewarding feature to implement, as it required careful state management and logic to prevent duplicate entries.

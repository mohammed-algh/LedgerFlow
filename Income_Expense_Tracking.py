from typing import List, Dict
import datetime
import pdfkit
import sqlite3


class IncomeExpenseTracking:

    def add_income(self, amount: float, description: str) -> None:
        """Add an income transaction."""
        transaction = {"date": datetime.date.today(),
                       "type": "income",
                       "amount": amount,
                       "description": description
                       }
        self.save_to_database(transaction)

    def add_expense(self, amount: float, description: str) -> None:
        """Add an expense transaction."""
        transaction = {"date": datetime.date.today(),
                       "type": "expense",
                       "amount": amount,
                       "description": description}
        self.save_to_database(transaction)

    def remove_transaction(self, transaction_id: int) -> bool:
        """Remove a transaction from the ledger using its ID."""
        with sqlite3.connect('ledgerflow.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            if cursor.rowcount == 0:
                conn.commit()
                return True
            else:
                return False

    def get_income(self) -> List[Dict]:
        """Return a list of all income transactions."""
        income = []
        transactions = self.load_from_database()
        for transaction in transactions:
            if transaction["type"] == "income":
                income.append(transaction)

        return income

    def get_expenses(self) -> List[Dict]:
        """Return a list of all expense transactions."""
        expenses = []
        transactions = self.load_from_database()
        for transaction in transactions:
            if transaction["type"] == "expense":
                expenses.append(transaction)

        return expenses

    def get_profit(self) -> float:
        """Return the profit (total income - total expenses)."""
        return self.get_total_income() - self.get_total_expenses()

    def get_total_income(self) -> float:
        """Return the total income."""
        income = self.get_income()

        return sum(transaction["amount"] for transaction in income)

    def get_total_expenses(self) -> float:
        """Return the total expenses."""
        expense = self.get_expenses()

        return sum(transaction["amount"] for transaction in expense)

    def get_balance(self) -> float:
        """Return the balance (total income - total expenses)."""
        return self.get_total_income() - self.get_total_expenses()

    def get_income_report(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Return a list of income transactions within a date range."""
        report = []
        income = self.get_income()
        for transaction in income:
            if start_date and transaction["date"] < datetime.datetime.strptime(start_date, '%Y-%m-%d').date():
                continue
            if end_date and transaction["date"] > datetime.datetime.strptime(end_date, '%Y-%m-%d').date():
                continue
            report.append(transaction)
        return report

    def get_expense_report(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Return a list of expense transactions within a date range."""
        report = []
        expense = self.get_expenses()
        for transaction in expense:
            if start_date and transaction["date"] < datetime.datetime.strptime(start_date, '%Y-%m-%d').date():
                continue
            if end_date and transaction["date"] > datetime.datetime.strptime(end_date, '%Y-%m-%d').date():
                continue
            report.append(transaction)
        return report

    def print_report(self, config) -> None:
        """Generate and print a PDF report of all transactions."""
        html = "<h1>Income and Expense Tracking Report</h1>\n"
        html += "<h2> Income Transactions</h2>\n"
        income = self.get_income()
        expense = self.get_expenses()
        for transaction in income:
            html += f"<p><b>ID:</b> {transaction['id']}<br><b>Date:</b> {transaction['date']}<br><b>Description:</b> {transaction['description']}<br><b>Amount:</b> ${transaction['amount']}</p>\n"
        html += "<h2>Expense Transactions</h2>\n"
        for transaction in expense:
            html += f"<p><b>ID:</b> {transaction['id']}<br><b>Date:</b> {transaction['date']}<br><b>Description:</b> {transaction['description']}<br><b>Amount:</b> ${transaction['amount']}</p>\n"
        html += f"<h2>Total Income: ${self.get_total_income()}</h2>\n"
        html += f"<h2>Total Expenses: ${self.get_total_expenses()}</h2>\n"
        html += f"<h2>Profit: ${self.get_profit()}</h2>\n"
        pdfkit.from_string(html, 'income_expense_report.pdf', configuration=config)

    def save_to_database(self, transaction) -> None:
        """Save all transactions to the database."""
        conn = sqlite3.connect('ledgerflow.db')
        c = conn.cursor()

        # Create transaction table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS transactions
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      date TEXT,
                      description TEXT,
                      amount REAL,
                      type TEXT)''')

        # Insert income
        c.execute("INSERT INTO transactions (date, description, amount, type) VALUES (?, ?, ?, ?)",
                  (transaction["date"], transaction["description"], transaction["amount"], transaction["type"]))

        conn.commit()
        conn.close()

    def load_from_database(self) -> list:
        """Load all transactions from the database."""
        conn = sqlite3.connect('ledgerflow.db')
        c = conn.cursor()

        # Retrieve transactions
        c.execute("SELECT * FROM transactions")
        rows = c.fetchall()

        transactions = []
        # Load transactions into memory
        for row in rows:
            transactions.append({"id": row[0], "date": row[1], "description": row[2], "amount": row[3], "type": row[4]})

        conn.close()
        return transactions

from typing import List, Dict
import datetime
import pdfkit


class IncomeExpenseTracking:
    def __init__(self):
        self.income = []
        self.expenses = []

    def add_income(self, amount: float, description: str) -> None:
        """Add an income transaction."""
        transaction = {"id": len(self.income) + 1,
                       "date": datetime.date.today(),
                       "amount": amount,
                       "description": description}
        self.income.append(transaction)

    def add_expense(self, amount: float, description: str) -> None:
        """Add an expense transaction."""
        transaction = {"id": len(self.expenses) + 1,
                       "date": datetime.date.today(),
                       "amount": amount,
                       "description": description}
        self.expenses.append(transaction)

    def delete_income(self, id: int) -> None:
        """Delete an income transaction by ID."""
        for i, transaction in enumerate(self.income):
            if transaction["id"] == id:
                del self.income[i]
                break

    def delete_expense(self, id: int) -> None:
        """Delete an expense transaction by ID."""
        for i, transaction in enumerate(self.expenses):
            if transaction["id"] == id:
                del self.expenses[i]
                break

    def get_income(self) -> List[Dict]:
        """Return a list of all income transactions."""
        return self.income

    def get_expenses(self) -> List[Dict]:
        """Return a list of all expense transactions."""
        return self.expenses

    def get_profit(self) -> float:
        """Return the profit (total income - total expenses)."""
        return self.get_total_income() - self.get_total_expenses()

    def get_total_income(self) -> float:
        """Return the total income."""
        return sum(transaction["amount"] for transaction in self.income)

    def get_total_expenses(self) -> float:
        """Return the total expenses."""
        return sum(transaction["amount"] for transaction in self.expenses)

    def get_balance(self) -> float:
        """Return the balance (total income - total expenses)."""
        return self.get_total_income() - self.get_total_expenses()

    def get_income_report(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Return a list of income transactions within a date range."""
        report = []
        for transaction in self.income:
            if start_date and transaction["date"] < datetime.datetime.strptime(start_date, '%Y-%m-%d').date():
                continue
            if end_date and transaction["date"] > datetime.datetime.strptime(end_date, '%Y-%m-%d').date():
                continue
            report.append(transaction)
        return report

    def get_expense_report(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Return a list of expense transactions within a date range."""
        report = []
        for transaction in self.expenses:
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
        for transaction in self.income:
            html += f"<p><b>ID:</b> {transaction['id']}<br><b>Date:</b> {transaction['date']}<br><b>Description:</b> {transaction['description']}<br><b>Amount:</b> ${transaction['amount']}</p>\n"
        html += "<h2>Expense Transactions</h2>\n"
        for transaction in self.expenses:
            html += f"<p><b>ID:</b> {transaction['id']}<br><b>Date:</b> {transaction['date']}<br><b>Description:</b> {transaction['description']}<br><b>Amount:</b> ${transaction['amount']}</p>\n"
        html += f"<h2>Total Income: ${self.get_total_income()}</h2>\n"
        html += f"<h2>Total Expenses: ${self.get_total_expenses()}</h2>\n"
        html += f"<h2>Profit: ${self.get_profit()}</h2>\n"
        pdfkit.from_string(html, 'income_expense_report.pdf', configuration=config)

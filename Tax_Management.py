from typing import List, Dict
import pdfkit
import sqlite3


class TaxManagement:
    def __init__(self, tax_rate: float):
        self.tax_rate = (tax_rate / 100)

    def get_income(self) -> List[Dict]:
        """Return a list of all income transactions."""
        income = []
        transactions = self.load_from_database()
        for transaction in transactions:
            if transaction["type"] == "income":
                income.append(transaction)

        return income

    def get_total_taxable_amount(self) -> float:
        """Return the total amount of taxable transactions."""
        income = self.get_income()
        return sum(transaction["amount"] for transaction in income)

    def get_total_tax(self) -> float:
        """Return the total tax owed."""
        return self.get_total_taxable_amount() * self.tax_rate

    def print_report(self, config) -> None:
        """Generate and print a PDF report of all tax transactions and tax owed."""
        html = "<h1>Tax Management Report</h1>\n"
        html += "<h2>Tax Transactions</h2>\n"
        income = self.get_income()
        for transaction in income:
            html += f"<p><b>ID:</b> {transaction['id']}<br><b>Date:</b> {transaction['date']}<br><b>Description:</b> {transaction['description']}<br><b>Amount:</b> ${transaction['amount']}</p>\n"
        html += f"<h2>Total Taxable Amount: ${self.get_total_taxable_amount()}</h2>\n"
        html += f"<h2>Tax Rate: {self.tax_rate * 100}%</h2>\n"
        html += f"<h2>Total Tax: ${self.get_total_tax()}</h2>\n"
        pdfkit.from_string(html, 'tax_report.pdf', configuration=config)

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

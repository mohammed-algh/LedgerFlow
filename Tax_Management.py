from typing import List, Dict
import datetime
import pdfkit


class TaxManagement:
    def __init__(self, tax_rate: float):
        self.tax_rate = tax_rate
        self.transactions = []

    def add_transaction(self, date: str, description: str, amount: float) -> None:
        """Add a tax transaction."""
        transaction = {"id": len(self.transactions) + 1,
                       "date": datetime.datetime.strptime(date, '%Y-%m-%d').date(),
                       "description": description,
                       "amount": amount}
        self.transactions.append(transaction)

    def get_transactions(self) -> List[Dict]:
        """Return a list of all tax transactions."""
        return self.transactions

    def get_total_taxable_amount(self) -> float:
        """Return the total amount of taxable transactions."""
        return sum(transaction["amount"] for transaction in self.transactions)

    def get_total_tax(self) -> float:
        """Return the total tax owed."""
        return self.get_total_taxable_amount() * self.tax_rate

    def print_report(self, config) -> None:
        """Generate and print a PDF report of all tax transactions and tax owed."""
        html = "<h1>Tax Management Report</h1>\n"
        html += "<h2>Tax Transactions</h2>\n"
        for transaction in self.transactions:
            html += f"<p><b>ID:</b> {transaction['id']}<br><b>Date:</b> {transaction['date']}<br><b>Description:</b> {transaction['description']}<br><b>Amount:</b> ${transaction['amount']}</p>\n"
        html += f"<h2>Total Taxable Amount: ${self.get_total_taxable_amount()}</h2>\n"
        html += f"<h2>Tax Rate: {self.tax_rate * 100}%</h2>\n"
        html += f"<h2>Total Tax: ${self.get_total_tax()}</h2>\n"
        pdfkit.from_string(html, 'tax_report.pdf', configuration=config)

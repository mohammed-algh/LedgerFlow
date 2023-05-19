from typing import List, Dict
import pdfkit
import sqlite3
from PyQt5.QtWidgets import QMessageBox, QWidget
import subprocess
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class TaxManagement (QWidget):
    def __init__(self, tax_rate: float):
        super().__init__()
        self.tax_rate = (tax_rate / 100)

    def update_table(self,ui) -> None:
        try:
            model = QStandardItemModel()
            model.setColumnCount(5)
            model.setHorizontalHeaderLabels(["ID", "Date", "Description", "Amount", "Type"])
            size = len(TaxManagement(1).get_income())
            for row, transaction in enumerate(TaxManagement(1).get_income()):
                                model.appendRow([
                                    QStandardItem(str(transaction['id'])),
                                    QStandardItem(transaction['date']),
                                    QStandardItem(transaction['description']),
                                    QStandardItem(str(transaction['amount'])),
                                    QStandardItem(transaction['type']),
                                    
                                ])

            ui.Tax_List.setModel(model)
            # Set the width of the columns
            ui.Tax_List.setColumnWidth(0, 50)  # ID column width
            ui.Tax_List.setColumnWidth(1, 200)  # Name column width
            ui.Tax_List.setColumnWidth(2, 317)  # Date column width
            if size <=5:
                ui.Tax_List.setColumnWidth(3, 100)  # Price column width
            else:
                ui.Tax_List.setColumnWidth(3, 83)  # Price column width
            ui.Tax_List.setColumnWidth(4, 100)  # Sal_val column width
            ui.Tax_List.setColumnWidth(5, 100)  # Sal_val column width
        except Exception as e:
                QMessageBox.warning(self, "Invalid Refresh", "Tax table is empty.")
    
    def get_income(self) -> List[Dict]:
        """Return a list of all income transactions."""
        income = []
        transactions = self.load_from_database()
        for transaction in transactions:
            if transaction["type"] == "Income":
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
        try:
            html = "<h1>Tax Management Report</h1>\n"
            html += "<h2>Tax Transactions</h2>\n"
            income = self.get_income()
            for transaction in income:
                html += f"<p><b>ID:</b> {transaction['id']}<br><b>Date:</b> {transaction['date']}<br><b>Description:</b> {transaction['description']}<br><b>Amount:</b> ${transaction['amount']}</p>\n"
            html += f"<h2>Total Taxable Amount: ${self.get_total_taxable_amount()}</h2>\n"
            html += f"<h2>Tax Rate: {self.tax_rate * 100}%</h2>\n"
            html += f"<h2>Total Tax: ${self.get_total_tax()}</h2>\n"
            pdfkit.from_string(html, 'tax_report.pdf', configuration=config)
            try:
                subprocess.run(['start', '', 'tax_report.pdf'], shell=True)
            except:
                QMessageBox.warning(self, "Failed Open Report", "Report cannot be opened.")
        except Exception as e:
            QMessageBox.warning(self, "Report Generation", "No transactions to be taxed and generated.")
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

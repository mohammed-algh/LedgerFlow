from typing import List, Dict
import datetime
import pdfkit
import sqlite3
from PyQt5.QtWidgets import QMessageBox, QWidget
import subprocess
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class IncomeExpenseTracking(QWidget):
    def updateTable(self, ui,type: str, checkbox: bool, date_start: str, date_end: str) -> None:
        try:
            model = QStandardItemModel()
            model.setColumnCount(5)
            model.setHorizontalHeaderLabels(["ID", "Date", "Description", "Amount", "Type"])
            size = 0
            
            if type == "":
                QMessageBox.warning(self, "Invalid Selection", "Please select the type of transaction to be displayed.")
            elif type == "All":
                if checkbox == False:
                    size = len(self.get_all())
                    for row, transaction in enumerate(self.get_all()):
                        model.appendRow([
                            QStandardItem(str(transaction['id'])),
                            QStandardItem(transaction['date']),
                            QStandardItem(transaction['description']),
                            QStandardItem(str(transaction['amount'])),
                            QStandardItem(transaction['type'])
                        ])
                else:
                    size = len(self.get_all_report(date_start,date_end))
                    for row, transaction in enumerate(self.get_all_report(date_start,date_end)):
                        model.appendRow([
                            QStandardItem(str(transaction['id'])),
                            QStandardItem(transaction['date']),
                            QStandardItem(transaction['description']),
                            QStandardItem(str(transaction['amount'])),
                            QStandardItem(transaction['type'])
                        ])
            elif type == "Income":
                if checkbox == False:
                    size = len(self.get_income())
                    for row, transaction in enumerate(self.get_income()):
                        model.appendRow([
                            QStandardItem(str(transaction['id'])),
                            QStandardItem(transaction['date']),
                            QStandardItem(transaction['description']),
                            QStandardItem(str(transaction['amount'])),
                            QStandardItem(transaction['type'])
                        ])
                else:
                    size = len(self.get_income_report(date_start,date_end))
                    for row, transaction in enumerate(self.get_income_report(date_start,date_end)):
                        model.appendRow([
                            QStandardItem(str(transaction['id'])),
                            QStandardItem(transaction['date']),
                            QStandardItem(transaction['description']),
                            QStandardItem(str(transaction['amount'])),
                            QStandardItem(transaction['type'])
                        ])
            else:
                if checkbox == False:
                    size = len(self.get_expenses())
                    for row, transaction in enumerate(self.get_expenses()):
                        model.appendRow([
                            QStandardItem(str(transaction['id'])),
                            QStandardItem(transaction['date']),
                            QStandardItem(transaction['description']),
                            QStandardItem(str(transaction['amount'])),
                            QStandardItem(transaction['type'])
                        ])
                else:
                    size = len(self.get_expense_report(date_start,date_end))
                    for row, transaction in enumerate(self.get_expense_report(date_start,date_end)):
                        model.appendRow([
                            QStandardItem(str(transaction['id'])),
                            QStandardItem(transaction['date']),
                            QStandardItem(transaction['description']),
                            QStandardItem(str(transaction['amount'])),
                            QStandardItem(transaction['type'])
                        ])

            ui.Transactions_tableView.setModel(model)
            
            # Set the width of the columns
            ui.Transactions_tableView.setColumnWidth(0, 30)  # ID column width
            ui.Transactions_tableView.setColumnWidth(1, 70)  # Date column width
            ui.Transactions_tableView.setColumnWidth(2, 180)  # Description column width
            ui.Transactions_tableView.setColumnWidth(3, 82)  # Amount column width
            ui.Transactions_tableView.setColumnWidth(4, 55)  # Type column width
            if size <= 5:#If list is 5 or less
                ui.Transactions_tableView.setColumnWidth(2, 180)  # Description column width
            else:
                ui.Transactions_tableView.setColumnWidth(2, 163)  # Description column width
        except Exception as e:
            QMessageBox.warning(self, "Table Display", "No transactions to be displayed.")


    def add_transaction(self, date, type: str, amount: float, description: str) -> None:
        """Add an income transaction."""
        if datetime.datetime.strptime(date, "%Y-%m-%d").date() > datetime.date.today():
            QMessageBox.warning(self, "Invalid Date", "Date cannot be in the future.")
        elif amount <= 0:
            QMessageBox.warning(self, "Invalid Amount", "Amount must be greater than zero.")
        elif description=="":
            QMessageBox.warning(self, "Missing Input", "Please provide a description for the transaction.")
        else:
            transaction = {"date": date,
                        "type": type,
                        "amount": amount,
                        "description": description
                        }
            self.save_to_database(transaction)
            QMessageBox.information(self, "Transaction Added!", "Transaction added successfully.")

    
    # def add_expense(self, amount: float, description: str) -> None:
    #     """Add an expense transaction."""
    #     transaction = {"date": datetime.date.today(),
    #                    "type": "expense",
    #                    "amount": amount,
    #                    "description": description}
    #     self.save_to_database(transaction)

    def remove_transaction(self, transaction_id: int) -> bool:
        """Remove a transaction from the ledger using its ID."""
        try:
            if not transaction_id:
                raise ValueError("ID field is empty")
            with sqlite3.connect('ledgerflow.db') as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
                if cursor.rowcount == 0:
                    conn.commit()
                    QMessageBox.warning(self, "Transaction Removal Failed!", "Transaction ID does not exist.")
                    return True
                else:
                    QMessageBox.information(self, "Transaction Removed!", "Transaction was removed successfully.")
                    return False
        except ValueError as e:
            QMessageBox.warning(self, "Invalid ID", str(e))
        except Exception as e:
            QMessageBox.warning(self, "Transaction Not Found", "There is no transaction with the given ID.")

    def get_income(self) -> List[Dict]:
        """Return a list of all income transactions."""
        income = []
        transactions = self.load_from_database()
        for transaction in transactions:
            if transaction["type"] == "Income":
                income.append(transaction)

        return income

    def get_expenses(self) -> List[Dict]:
        """Return a list of all expense transactions."""
        expenses = []
        transactions = self.load_from_database()
        for transaction in transactions:
            if transaction["type"] == "Expense":
                expenses.append(transaction)

        return expenses
    def get_all(self) -> List[Dict]:
        """Return a list of all expense transactions."""
        all = []
        transactions = self.load_from_database()
        for transaction in transactions:
            all.append(transaction)

        return all

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

    def get_income_report(self, start_date_str: str = None, end_date_str: str = None) -> List[Dict]:
        """Return a list of income transactions within a date range."""
        report = []
        income = self.get_income()

        if start_date_str:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = None

        if end_date_str:
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = None

        for transaction in income:
            transaction_date_str = transaction["date"]
            transaction_date = datetime.datetime.strptime(transaction_date_str, '%Y-%m-%d').date()

            if start_date and transaction_date < start_date:
                continue
            if end_date and transaction_date > end_date:
                continue

            report.append(transaction)

        return report

    def get_expense_report(self, start_date_str: str = None, end_date_str: str = None) -> List[Dict]:
        """Return a list of expense transactions within a date range."""
        report = []
        expense = self.get_expenses()

        if start_date_str:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = None

        if end_date_str:
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = None

        for transaction in expense:
            transaction_date_str = transaction["date"]
            transaction_date = datetime.datetime.strptime(transaction_date_str, '%Y-%m-%d').date()

            if start_date and transaction_date < start_date:
                continue
            if end_date and transaction_date > end_date:
                continue

            report.append(transaction)

        return report
    def get_all_report(self, start_date_str: str = None, end_date_str: str = None) -> List[Dict]:
        """Return a list of income transactions within a date range."""
        report = []
        all = self.get_all()

        if start_date_str:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = None

        if end_date_str:
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = None

        for transaction in all:
            transaction_date_str = transaction["date"]
            transaction_date = datetime.datetime.strptime(transaction_date_str, '%Y-%m-%d').date()

            if start_date and transaction_date < start_date:
                continue
            if end_date and transaction_date > end_date:
                continue

            report.append(transaction)

        return report
    def print_report(self, config) -> None:
        """Generate and print a PDF report of all transactions."""
        try:
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
            try:
                subprocess.run(['start', '', 'income_expense_report.pdf'], shell=True)
            except:
                QMessageBox.warning(self, "Failed Open Report", "Report cannot be opened.")
        except Exception as e:
            QMessageBox.warning(self, "Report Generation", "No transactions to be generated.")
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

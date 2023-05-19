from typing import List, Dict
import datetime
import pdfkit
import sqlite3
from PyQt5.QtWidgets import QMessageBox, QWidget
import subprocess
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class PayrollManagement(QWidget):
    def update_table(self,ui) -> None:
        try:
            model = QStandardItemModel()
            model.setColumnCount(4)
            model.setHorizontalHeaderLabels(["ID", "Name", "Salary", "Start Date"])
            size = len(self.get_employees())
            for row, employee in enumerate(self.get_employees()):
                                model.appendRow([
                                    QStandardItem(str(employee['id'])),
                                    QStandardItem(employee['name']),
                                    QStandardItem(str(employee['salary'])),
                                    QStandardItem(employee['start_date'])
                                ])

            ui.Employee_List.setModel(model)
            # Set the width of the columns
            ui.Employee_List.setColumnWidth(0, 10)  # ID column width
            if size <=6:
                ui.Employee_List.setColumnWidth(1, 150)  # Name column width
            else:
                ui.Employee_List.setColumnWidth(1, 133)  # Name column width
            
            ui.Employee_List.setColumnWidth(2, 95)  # Salary column width
            ui.Employee_List.setColumnWidth(3, 80)  # Start date column width
        except Exception as e:
                QMessageBox.warning(self, "Invalid Refresh", "No employees are hired in the company.")

    def add_employee(self, name: str, salary: float, start_date: str) -> None:
        """Add an employee."""
        if name=="":
            QMessageBox.warning(self, "Missing Input", "Please provide a name for the employee.")
        elif salary <= 0:
            QMessageBox.warning(self, "Invalid Salary", "Salary must be greater than zero.")
        else:
            employee = {"name": name,
                    "salary": salary,
                    "start_date": datetime.datetime.strptime(start_date, '%Y-%m-%d').date(),
                    }
            self.save_to_database(employee)
            QMessageBox.information(self, "Employee Hired!", "Congratulations! A new employee has been hired.")
        

    def terminate_employee(self, id: str) -> bool:
        """Remove a employees from the database using its ID."""
        employee_id = int(id)
        with sqlite3.connect('ledgerflow.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
            if cursor.rowcount == 0:
                conn.commit()
                return True
            else:
                return False

    def get_employees(self):
        """Return a list of all employees."""
        return self.load_from_database()

    def get_employee(self, id: int):
        """Return an employee by ID."""
        employees = self.load_from_database()

        for employee in employees:
            if employee["id"] == id:
                return employee
        return None

    def get_employee_salary(self, id: int):
        """Return an employee's salary by ID."""
        employees = self.load_from_database()

        for employee in employees:
            if employee["id"] == id:
                return employee["salary"]
        return None

    def get_total_payroll(self) -> float:
        """Return the total payroll (sum of all employee salaries)."""
        employees = self.load_from_database()
        return sum(employee["salary"] for employee in employees)

    def print_report(self, config) -> None:
        """Generate and print a PDF report of all employees and their salaries."""
        try:
            html = "<h1>Payroll Management Report</h1>\n"
            employees = self.load_from_database()

            for employee in employees:
                html += f"<p><b>ID:</b> {employee['id']}<br><b>Name:</b> {employee['name']}<br><b>Salary:</b> ${employee['salary']}</p>\n"
            html += f"<h2>Total Payroll: ${self.get_total_payroll()}</h2>\n"
            pdfkit.from_string(html, 'payroll_report.pdf', configuration=config)
            try:
                subprocess.run(['start', '', 'payroll_report.pdf'], shell=True)
            except:
                QMessageBox.warning(self, "Failed Open Report", "Report cannot be opened.")
        except Exception as e:
            QMessageBox.warning(self, "Report Generation", "No employees are hired to generate a payroll report for them.")
    def save_to_database(self, employee) -> None:
        """Save all employees to the database."""
        conn = sqlite3.connect('ledgerflow.db')
        c = conn.cursor()

        # Create employees table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS employees
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT,
                      salary REAL,
                      start_date TEXT)''')

        # Insert employee
        c.execute("INSERT INTO employees (name, salary, start_date) VALUES (?, ?, ?)",
                  (employee["name"], employee["salary"], employee["start_date"]))

        conn.commit()
        conn.close()

    def load_from_database(self) -> list:
        """Load all employees from the database."""
        conn = sqlite3.connect('ledgerflow.db')
        c = conn.cursor()

        # Retrieve employees
        c.execute("SELECT * FROM employees")
        rows = c.fetchall()

        employees = []
        # Load employees into memory
        for row in rows:
            employees.append({"id": row[0], "name": row[1], "salary": row[2], "start_date": row[3]})

        conn.close()
        return employees

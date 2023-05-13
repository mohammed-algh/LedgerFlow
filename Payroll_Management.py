from typing import List, Dict
import datetime
import pdfkit


class PayrollManagement:
    def __init__(self):
        self.employees = []

    def add_employee(self, name: str, salary: float, start_date: str) -> None:
        """Add an employee."""
        employee = {"id": len(self.employees) + 1,
                    "name": name,
                    "salary": salary,
                    "start_date": datetime.datetime.strptime(start_date, '%Y-%m-%d').date(),
                    "end_date": None}
        self.employees.append(employee)

    def terminate_employee(self, id: int, end_date: str) -> None:
        """Terminate an employee by ID."""
        for employee in self.employees:
            if employee["id"] == id:
                employee["end_date"] = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
                break

    def get_employees(self):
        """Return a list of all employees."""
        return self.employees

    def get_employee(self, id: int):
        """Return an employee by ID."""
        for employee in self.employees:
            if employee["id"] == id:
                return employee
        return None

    def get_employee_salary(self, id: int):
        """Return an employee's salary by ID."""
        for employee in self.employees:
            if employee["id"] == id:
                return employee["salary"]
        return None

    def get_total_payroll(self) -> float:
        """Return the total payroll (sum of all employee salaries)."""
        return sum(employee["salary"] for employee in self.employees)

    def get_payroll_report(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Return a list of employees and their salaries within a date range."""
        report = []
        for employee in self.employees:
            if start_date and employee["start_date"] > datetime.datetime.strptime(start_date, '%Y-%m-%d').date():
                continue
            if end_date and (employee["end_date"] is None or employee["end_date"] < datetime.datetime.strptime(end_date,
                                                                                                               '%Y-%m-%d').date()):
                continue
            report.append({"name": employee["name"], "salary": employee["salary"]})
        return report

    def print_report(self, config) -> None:
        """Generate and print a PDF report of all employees and their salaries."""
        html = "<h1>Payroll Management Report</h1>\n"
        for employee in self.employees:
            html += f"<p><b>ID:</b> {employee['id']}<br><b>Name:</b> {employee['name']}<br><b>Salary:</b> ${employee['salary']}</p>\n"
        html += f"<h2>Total Payroll: ${self.get_total_payroll()}</h2>\n"
        pdfkit.from_string(html, 'payroll_report.pdf', configuration=config)

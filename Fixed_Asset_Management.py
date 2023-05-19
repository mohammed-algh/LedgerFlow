from typing import List, Dict
import datetime
import pdfkit
import sqlite3
from PyQt5.QtWidgets import QMessageBox, QWidget
import subprocess
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QDate

class FixedAssetManagement(QWidget):
    def update_table(self,ui) -> None:
        try:
            model = QStandardItemModel()
            model.setColumnCount(6)
            model.setHorizontalHeaderLabels(["ID", "Name", "Date", "Price", "Salvage Val", "Years"])
            size = len(FixedAssetManagement().get_assets())
            for row, asset in enumerate(FixedAssetManagement().get_assets()):
                                model.appendRow([
                                    QStandardItem(str(asset['id'])),
                                    QStandardItem(asset['name']),
                                    QStandardItem(str(asset['purchase_date'])),
                                    QStandardItem(str(asset['purchase_price'])),
                                    QStandardItem(str(asset['salvage_value'])),
                                    QStandardItem(str(asset['life_years']))
                                ])

            ui.Asset_List.setModel(model)
            # Set the width of the columns
            ui.Asset_List.setColumnWidth(0, 5)  # ID column width
            ui.Asset_List.setColumnWidth(1, 84)  # Name column width
            ui.Asset_List.setColumnWidth(2, 70)  # Date column width
            if size <=5:
                ui.Asset_List.setColumnWidth(3, 59)  # Price column width
            else:
                ui.Asset_List.setColumnWidth(3, 42)  # Price column width
            ui.Asset_List.setColumnWidth(4, 70)  # Sal_val column width
            ui.Asset_List.setColumnWidth(5, 30)  # Life years column width
        except Exception as e:
                QMessageBox.warning(self, "Invalid Refresh", "Asset table is empty.")

    def add_asset(self, name: str, purchase_price: float, salvage_value: float,
                  life_years: int, purchase_date: str) -> None:
        """Add a fixed asset."""
        if name=="":
            QMessageBox.warning(self, "Missing Input", "Please provide a name for the asset.")
        elif datetime.datetime.strptime(purchase_date, "%Y-%m-%d").date() > datetime.date.today():
            QMessageBox.warning(self, "Invalid Date", "Date cannot be in the future.")
        elif purchase_price <= 0 or salvage_value <= 0 or life_years <= 0:
            QMessageBox.warning(self, "Invalid Amount", "price or salvage value must be greater than zero.")
        else:
            asset = {"name": name,
                 "purchase_date": datetime.datetime.strptime(purchase_date, '%Y-%m-%d').date(),
                 "purchase_price": purchase_price,
                 "salvage_value": salvage_value,
                 "life_years": life_years}
            self.save_to_database(asset)
            QMessageBox.information(self, "Transaction Added!", "Transaction added successfully.")
        

    def get_assets(self) -> List[Dict]:
        """Return a list of all fixed assets."""
        return self.load_from_database()

    def get_asset(self,ui, id: int):
        """Return a fixed asset by ID."""
        assets = self.get_assets()
        for asset in assets:
            if asset["id"] == id:
                searched_asset = asset
                ui.name_field_Asset.setText(searched_asset["name"])
                ui.price_field_Asset.setValue(float(searched_asset["purchase_price"]))
                ui.sal_val_field_Asset.setValue(float(searched_asset["salvage_value"]))
                ui.year_field_Asset.setValue(float(searched_asset["life_years"]))
                ui.date_field_Asset.date().toString("yyyy-MM-dd")
                date = QDate.fromString(searched_asset["purchase_date"], "yyyy-MM-dd")
                ui.date_field_Asset.setDate(date)
        return None

    def get_total_depreciation(self, id: int):
        """Return the total depreciation of a fixed asset by ID."""
        asset = self.get_asset(id)
        if asset is None:
            return None
        purchase_date = datetime.datetime.strptime(asset["purchase_date"], "%Y-%m-%d").date()
        years = (datetime.date.today() - purchase_date).days / 365
        depreciation = (asset["purchase_price"] / float(asset["life_years"])) * years
        return round(depreciation)

    def print_report(self, config) -> None:
        """Generate and print a PDF report of all fixed assets and their depreciation."""
    
        html = "<h1>Fixed Asset Management Report</h1>\n"
        html += "<h2>Fixed Assets</h2>\n"
        assets = self.load_from_database()
        for asset in assets:
            html += f"<p><b>ID:</b> {asset['id']}<br><b>Name:</b> {asset['name']}<br><b>Purchase Date:</b> {asset['purchase_date']}<br><b>Purchase Price:</b> ${asset['purchase_price']}<br><b>Salvage Value:</b> ${asset['salvage_value']}<br><b>Life (years):</b> {asset['life_years']}<br><b>Total Depreciation:</b> ${self.get_total_depreciation(asset['id'])}</p>\n"
        pdfkit.from_string(html, 'fixed_asset_report.pdf', configuration=config)
        try:
            subprocess.run(['start', '', 'fixed_asset_report.pdf'], shell=True)
        except:
            print(f"Unable to open the PDF file: {'fixed_asset_report.pdf'}")
       
    def save_to_database(self, fixed_asset) -> None:
        """Save all fixed_assets to the database."""
        conn = sqlite3.connect('ledgerflow.db')
        c = conn.cursor()

        # Create fixed_assets table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS fixed_assets
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT,
                      purchase_date TEXT,
                      purchase_price REAL,
                      salvage_value REAL,
                      life_years REAL)''')

        # Insert assets
        c.execute(
            "INSERT INTO fixed_assets (name, purchase_date, purchase_price, salvage_value, life_years) VALUES (?, ?, ?, ?, ?)",
            (fixed_asset["name"], fixed_asset["purchase_date"], fixed_asset["purchase_price"],
             fixed_asset["salvage_value"], fixed_asset["life_years"]))

        conn.commit()
        conn.close()

    def load_from_database(self) -> list:
        """Load all fixed_assets from the database."""
        conn = sqlite3.connect('ledgerflow.db')
        c = conn.cursor()

        # Retrieve fixed assets
        c.execute("SELECT * FROM fixed_assets")
        rows = c.fetchall()

        assets = []
        # Load fixed assets into memory
        for row in rows:
            assets.append({"id": row[0], "name": row[1], "purchase_date": row[2], "purchase_price": row[3],
                           "salvage_value": row[4], "life_years": "{:.1f}".format(row[5])})

        conn.close()
        return assets

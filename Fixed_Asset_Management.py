from typing import List, Dict
import datetime
import pdfkit
import sqlite3


class FixedAssetManagement:

    def add_asset(self, name: str, purchase_price: float, salvage_value: float,
                  life_years: int, purchase_date=str(datetime.date.today())) -> None:
        """Add a fixed asset."""
        asset = {"name": name,
                 "purchase_date": datetime.datetime.strptime(purchase_date, '%Y-%m-%d').date(),
                 "purchase_price": purchase_price,
                 "salvage_value": salvage_value,
                 "life_years": life_years}
        self.save_to_database(asset)

    def get_assets(self) -> List[Dict]:
        """Return a list of all fixed assets."""
        return self.load_from_database()

    def get_asset(self, id: int):
        """Return a fixed asset by ID."""
        assets = self.get_assets()
        for asset in assets:
            if asset["id"] == id:
                return asset
        return None

    def get_total_depreciation(self, id: int):
        """Return the total depreciation of a fixed asset by ID."""
        asset = self.get_asset(id)
        if asset is None:
            return None
        purchase_date = datetime.datetime.strptime(asset["purchase_date"], "%Y-%m-%d").date()
        years = (datetime.date.today() - purchase_date).days / 365
        depreciation = (asset["purchase_price"] / asset["life_years"]) * years
        return round(depreciation)

    def print_report(self, config) -> None:
        """Generate and print a PDF report of all fixed assets and their depreciation."""
        html = "<h1>Fixed Asset Management Report</h1>\n"
        html += "<h2>Fixed Assets</h2>\n"
        assets = self.load_from_database()
        for asset in assets:
            html += f"<p><b>ID:</b> {asset['id']}<br><b>Name:</b> {asset['name']}<br><b>Purchase Date:</b> {asset['purchase_date']}<br><b>Purchase Price:</b> ${asset['purchase_price']}<br><b>Salvage Value:</b> ${asset['salvage_value']}<br><b>Life (years):</b> {asset['life_years']}<br><b>Total Depreciation:</b> ${self.get_total_depreciation(asset['id'])}</p>\n"
        pdfkit.from_string(html, 'fixed_asset_report.pdf', configuration=config)

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
                           "salvage_value": row[4], "life_years": row[5]})

        conn.close()
        return assets

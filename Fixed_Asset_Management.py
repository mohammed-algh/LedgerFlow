from typing import List, Dict
import datetime
import pdfkit


class FixedAssetManagement:
    def __init__(self):
        self.assets = []

    def add_asset(self, name: str, purchase_date: str, purchase_price: float, salvage_value: float,
                  life_years: int) -> None:
        """Add a fixed asset."""
        asset = {"id": len(self.assets) + 1,
                 "name": name,
                 "purchase_date": datetime.datetime.strptime(purchase_date, '%Y-%m-%d').date(),
                 "purchase_price": purchase_price,
                 "salvage_value": salvage_value,
                 "life_years": life_years}
        self.assets.append(asset)

    def get_assets(self) -> List[Dict]:
        """Return a list of all fixed assets."""
        return self.assets

    def get_asset(self, id: int):
        """Return a fixed asset by ID."""
        for asset in self.assets:
            if asset["id"] == id:
                return asset
        return None

    def get_total_depreciation(self, id: int):
        """Return the total depreciation of a fixed asset by ID."""
        asset = self.get_asset(id)
        if asset is None:
            return None
        years = (datetime.date.today() - asset["purchase_date"]).days / 365
        if years > asset["life_years"]:
            depreciation_per_year = (asset["purchase_price"] - asset["salvage_value"]) / asset["life_years"]
            return depreciation_per_year * years

    def print_report(self, config) -> None:
        """Generate and print a PDF report of all fixed assets and their depreciation."""
        html = "<h1>Fixed Asset Management Report</h1>\n"
        html += "<h2>Fixed Assets</h2>\n"
        for asset in self.assets:
            html += f"<p><b>ID:</b> {asset['id']}<br><b>Name:</b> {asset['name']}<br><b>Purchase Date:</b> {asset['purchase_date']}<br><b>Purchase Price:</b> ${asset['purchase_price']}<br><b>Salvage Value:</b> ${asset['salvage_value']}<br><b>Life (years):</b> {asset['life_years']}<br><b>Total Depreciation:</b> ${self.get_total_depreciation(asset['id'])}</p>\n"
        pdfkit.from_string(html, 'fixed_asset_report.pdf', configuration=config)

import pdfkit
from Income_Expense_Tracking import IncomeExpenseTracking
from Payroll_Management import PayrollManagement
from Tax_Management import TaxManagement
from Fixed_Asset_Management import FixedAssetManagement
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from layout import Ui_MainWindow
config = pdfkit.configuration(wkhtmltopdf='wkhtmltopdf/bin/wkhtmltopdf.exe')


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LedgerFlow_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ##################################################################################
    ############################## Moving between pages ##############################
    ##################################################################################

    ui.In_ex_Button.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(1))
    ui.fix_asset_Button.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(2))
    ui.tax_Button.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(3))
    ui.payroll_Button.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(4))
    ui.homepage_in_ex.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(0))
    ui.home_fixed.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(0))
    ui.home_tax.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(0))
    ui.home_payroll.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(0))
    ui.in_ex_fixed.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(1))
    ui.in_ex_tax.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(1))
    ui.in_ex_payroll.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(1))
    ui.fixed_in_ex.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(2))
    ui.fixed_tax.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(2))
    ui.fixed_payroll.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(2))
    ui.tax_in_ex.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(3))
    ui.tax_fixed.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(3))
    ui.tax_payroll.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(3))
    ui.payroll_in_ex.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(4))
    ui.pay_fixed.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(4))
    ui.payroll_tax.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(4))

    ###################################################################################
    ############################## Income & Expense Page ##############################
    ###################################################################################

    current_date = QtCore.QDate.currentDate()
    ui.in_ex_date.setDate(current_date)
    ui.in_ex_date_start.setDate(current_date)
    ui.in_ex_date_end.setDate(current_date)

    #Add a new transaction
    ui.add_in_ex_Button.clicked.connect(lambda: IncomeExpenseTracking().add_transaction(ui.in_ex_date.date().toString("yyyy-MM-dd"),ui.in_ex_type.currentText(), ui.in_ex_amount.value(), ui.in_ex_desc.toPlainText()))
    
    #Show Table
    ui.show_trans_Button.clicked.connect(lambda: IncomeExpenseTracking().updateTable(
        ui,
        ui.in_ex_type2.currentText(),
        ui.checkBox.isChecked(),
        ui.in_ex_date_start.date().toString("yyyy-MM-dd"),
        ui.in_ex_date_end.date().toString("yyyy-MM-dd")))

    #Remove a transaction by ID
    ui.remove_trans_Button.clicked.connect(lambda: IncomeExpenseTracking().remove_transaction(ui.trans_ID_field.text()))

    #Generate a report
    ui.print_trans_Button.clicked.connect(lambda: IncomeExpenseTracking().print_report(config))

    #Initializing the table
    model = QStandardItemModel()
    model.setColumnCount(5)
    model.setHorizontalHeaderLabels(["ID", "Date", "Description", "Amount", "Type"])
    ui.Transactions_tableView.setModel(model)
    ui.Transactions_tableView.setColumnWidth(0, 30)  # ID column width
    ui.Transactions_tableView.setColumnWidth(1, 70)  # Date column width
    ui.Transactions_tableView.setColumnWidth(2, 180)  # Description column width
    ui.Transactions_tableView.setColumnWidth(3, 85)  # Amount column width
    ui.Transactions_tableView.setColumnWidth(4, 52)  # Type column width

    #########################################################################################
    ############################## Fixed Asset Management Page ##############################
    #########################################################################################

    ui.date_field_Asset.setDate(current_date)
    # Create the table
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
            None

    #Add a new transaction
    ui.add_Asset_Button.clicked.connect(lambda: FixedAssetManagement().add_asset(
        ui.name_field_Asset.text(),
        ui.price_field_Asset.value(),
        ui.sal_val_field_Asset.value(),
        ui.year_field_Asset.value(),
        ui.date_field_Asset.date().toString("yyyy-MM-dd")),
        )
    FixedAssetManagement.get_assets()
    #Search for an Asset
    ui.search_Asset_Button.clicked.connect(lambda: FixedAssetManagement().get_asset_to_print(ui,ui.ID_field_Asset.text()))

    #Refresh Table
    ui.asset_refresh_Button.clicked.connect(lambda: FixedAssetManagement().update_table(ui))

    #Generate a Report
    ui.print_Asset_Button.clicked.connect(lambda: FixedAssetManagement().print_report(config))

    #Search a Depreciation by ID
    ui.dep_search_Button.clicked.connect(lambda: FixedAssetManagement().get_one_asset_depreciation_to_print(ui,ui.dep_ID_field_Asset.text()))


    #################################################################################
    ############################## Tax Management Page ##############################
    #################################################################################
    
    # Create the table
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
            None
    
    #Refresh Table
    ui.tax_refresh_Button.clicked.connect(lambda: TaxManagement(ui.tax_rate.value()).update_table(ui))

    #Generate Tax Report
    ui.print_tax_Button.clicked.connect(lambda: TaxManagement(ui.tax_rate.value()).print_report(config))


    ################################################################################
    ############################## Payroll Management ##############################
    ################################################################################
    ui.employee_s_date.setDate(current_date)


    #Create the table
    try:
        model = QStandardItemModel()
        model.setColumnCount(4)
        model.setHorizontalHeaderLabels(["ID", "Name", "Salary", "Start Date"])
        size = len(PayrollManagement().get_employees())
        for row, employee in enumerate(PayrollManagement().get_employees()):
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
            None
    
    #Add a new employee
    ui.add_emp_Button.clicked.connect(lambda: PayrollManagement().add_employee(ui.name_emp_field.text(), ui.employee_sal_field.value(),ui.employee_s_date.date().toString("yyyy-MM-dd")))
    
    #Delete an employee
    ui.remove_emp_Button.clicked.connect(lambda: PayrollManagement().terminate_employee(ui.employee_ID_field.text()))

    #Search for an employee
    ui.search_emp_Button.clicked.connect(lambda: PayrollManagement().get_employee_to_print(ui,ui.employee_ID_field.text()))
    
    #Refresh the employees list
    ui.refresh_emp_Button.clicked.connect(lambda: PayrollManagement().update_table(ui))
    
    #Refresh the employees list
    ui.print_emp_Button.clicked.connect(lambda: PayrollManagement().print_report(config))

    #############################################################################
    ############################## Show MainWindow ##############################
    #############################################################################
    MainWindow.show()
    sys.exit(app.exec_())

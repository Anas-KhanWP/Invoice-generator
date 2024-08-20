import sys
import random
import os
import base64
import asyncio
from playwright.async_api import async_playwright
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QVBoxLayout, 
    QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QCalendarWidget, QGridLayout, QMessageBox, QInputDialog, QFileDialog, QGroupBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QPalette, QColor


class InvoiceApp(QWidget):
    def __init__(self):
        super().__init__()

        # Generate a random invoice number
        self.invoice_number = random.randint(100000, 999999)

        # Initialize UI components
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Invoice Application")
        self.setGeometry(100, 100, 900, 700)

        # Set up the palette for colors
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#f0f0f0"))
        self.setPalette(palette)

        main_layout = QVBoxLayout()

        # Font settings
        header_font = QFont("Arial", 14)
        label_font = QFont("Arial", 11)
        input_font = QFont("Arial", 10)

        # Header Section
        header_layout = QVBoxLayout()
        self.add_header(header_layout)
        main_layout.addLayout(header_layout)

        # Invoice Information Group Box
        invoice_group = QGroupBox("Invoice Information")
        invoice_group.setStyleSheet("background-color: #e6f2ff; border: 1px solid #007bff;")
        invoice_layout = QGridLayout()
        invoice_group.setLayout(invoice_layout)

        # Invoice Number
        invoice_label = QLabel("Invoice #")
        invoice_label.setFont(header_font)
        invoice_layout.addWidget(invoice_label, 0, 0)

        self.invoice_number_label = QLabel(str(self.invoice_number))
        self.invoice_number_label.setFont(header_font)
        invoice_layout.addWidget(self.invoice_number_label, 0, 1)

        # Date
        date_label = QLabel("Date")
        date_label.setFont(header_font)
        invoice_layout.addWidget(date_label, 1, 0)

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.setFont(label_font)
        invoice_layout.addWidget(self.calendar, 1, 1)

        # Venue
        venue_label = QLabel("Venue")
        venue_label.setFont(header_font)
        invoice_layout.addWidget(venue_label, 2, 0)

        self.venue_input = QLineEdit()
        self.venue_input.setPlaceholderText("Enter the venue for the invoice")
        self.venue_input.setFont(input_font)
        invoice_layout.addWidget(self.venue_input, 2, 1)

        main_layout.addWidget(invoice_group)

        # Client Information Group Box
        client_info_group = QGroupBox("Client Information")
        client_info_group.setStyleSheet("background-color: #e6ffcc; border: 1px solid #28a745;")
        client_info_layout = QGridLayout()
        client_info_group.setLayout(client_info_layout)

        client_info_title = QLabel("Client Information")
        client_info_title.setFont(header_font)
        client_info_layout.addWidget(client_info_title, 0, 0, 1, 2)

        # Client Name
        client_name_label = QLabel("Client Name")
        client_name_label.setFont(label_font)
        client_info_layout.addWidget(client_name_label, 1, 0)

        self.client_name_input = QLineEdit()
        self.client_name_input.setPlaceholderText("Enter the client's name")
        self.client_name_input.setFont(input_font)
        client_info_layout.addWidget(self.client_name_input, 1, 1)

        # Phone Number
        phone_number_label = QLabel("Phone Number")
        phone_number_label.setFont(label_font)
        client_info_layout.addWidget(phone_number_label, 2, 0)

        self.phone_number_input = QLineEdit()
        self.phone_number_input.setPlaceholderText("Enter the client's phone number")
        self.phone_number_input.setFont(input_font)
        client_info_layout.addWidget(self.phone_number_input, 2, 1)

        # Bill To
        bill_to_label = QLabel("Bill To")
        bill_to_label.setFont(label_font)
        client_info_layout.addWidget(bill_to_label, 3, 0)

        self.bill_to_input = QLineEdit()
        self.bill_to_input.setPlaceholderText("Enter the billing address")
        self.bill_to_input.setFont(input_font)
        client_info_layout.addWidget(self.bill_to_input, 3, 1)

        main_layout.addWidget(client_info_group)

        # Items Section
        item_section_group = QGroupBox("Item Details")
        item_section_group.setStyleSheet("background-color: #ffffcc; border: 1px solid #ffc107;")
        item_section_layout = QVBoxLayout()
        item_section_group.setLayout(item_section_layout)

        # Table for Items
        self.item_table = QTableWidget(0, 5)
        self.item_table.setFont(input_font)
        self.item_table.setHorizontalHeaderLabels(["Item", "Description", "Rate", "Quantity", "Price"])
        self.item_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        item_section_layout.addWidget(self.item_table)

        # Add/Remove Item Buttons
        item_button_layout = QHBoxLayout()

        self.add_item_button = QPushButton("Add Item")
        self.add_item_button.setFont(label_font)
        self.add_item_button.setToolTip("Add a new item to the invoice")
        self.add_item_button.clicked.connect(self.add_item)
        item_button_layout.addWidget(self.add_item_button)

        self.remove_item_button = QPushButton("Remove Selected")
        self.remove_item_button.setFont(label_font)
        self.remove_item_button.setToolTip("Remove the selected item from the invoice")
        self.remove_item_button.clicked.connect(self.remove_item)
        item_button_layout.addWidget(self.remove_item_button)

        item_section_layout.addLayout(item_button_layout)
        main_layout.addWidget(item_section_group)

        # Save and Clear Buttons
        action_button_layout = QHBoxLayout()

        self.save_button = QPushButton("Save Invoice")
        self.save_button.setFont(label_font)
        self.save_button.setToolTip("Save the invoice")
        self.save_button.clicked.connect(self.save_invoice_button_clicked)
        action_button_layout.addWidget(self.save_button)

        self.clear_button = QPushButton("Clear All Fields")
        self.clear_button.setFont(label_font)
        self.clear_button.setToolTip("Clear all the input fields")
        self.clear_button.clicked.connect(self.clear_form)
        action_button_layout.addWidget(self.clear_button)

        main_layout.addLayout(action_button_layout)

        self.setLayout(main_layout)
    
    def add_header(self, layout):
        """ Adds a header to the UI with company name and logo. """
        header_layout = QHBoxLayout()
        logo_label = QLabel("💼")  # Placeholder for logo
        logo_label.setFont(QFont("Arial", 20))
        header_layout.addWidget(logo_label)
        
        title_label = QLabel("Company Name")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: darkblue;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        layout.addLayout(header_layout)

    def add_item(self):
        """ Opens a dialog for adding item details. """
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Add Item")
        dialog.setLabelText("Enter item details (format: Name, Description, Rate, Quantity):")
        dialog.setTextValue("Item Name, Item Description, 0.00, 1")
        dialog.setOkButtonText("Add Item")
        
        if dialog.exec_() == QInputDialog.Accepted:
            item_details = dialog.textValue()
            try:
                item_name, item_description, rate, quantity = [x.strip() for x in item_details.split(',')]
                rate = float(rate)
                quantity = float(quantity)
                price = rate * quantity

                # Add a new row to the item table
                row_position = self.item_table.rowCount()
                self.item_table.insertRow(row_position)

                # Insert item details into the row
                self.item_table.setItem(row_position, 0, QTableWidgetItem(item_name))
                self.item_table.setItem(row_position, 1, QTableWidgetItem(item_description))
                self.item_table.setItem(row_position, 2, QTableWidgetItem(f"{rate:.2f}"))
                self.item_table.setItem(row_position, 3, QTableWidgetItem(f"{quantity:.2f}"))
                self.item_table.setItem(row_position, 4, QTableWidgetItem(f"{price:.2f}"))
            except Exception as e:
                QMessageBox.warning(self, "Invalid Input", "Please enter valid item details in the correct format.")
    
    def remove_item(self):
        """ Remove the selected row from the item table """
        current_row = self.item_table.currentRow()
        if current_row >= 0:
            self.item_table.removeRow(current_row)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a row to remove.")

    def get_number_input(self, message, title):
        """ Utility function to get number input from the user """
        text, ok = QInputDialog.getText(self, title, message)
        if ok:
            try:
                value = float(text)
                return value, True
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")
                return 0, False
        return 0, False

    def save_invoice_button_clicked(self):
        """ Handle the Save Invoice button click """
        asyncio.run(self.save_invoice())

    async def save_invoice(self):
        """ Save the invoice as a PDF and provide feedback """
        await self.file_to_pdf()

        # This could involve saving to a file or database
        QMessageBox.information(self, "Invoice Saved", "The invoice has been saved successfully!")
        print("Invoice saved!")

    def clear_form(self):
        """ Clear all input fields and reset the item table """
        self.venue_input.clear()
        self.client_name_input.clear()
        self.phone_number_input.clear()
        self.bill_to_input.clear()
        self.item_table.setRowCount(0)

    async def file_to_pdf(self):
        """ Generate a PDF from the invoice HTML content """
        try:
            html_content = self.generate_invoice_html()
            
            pdf_directory = "./invoices/"
            
            # Create the directory if it does not exist
            if not os.path.exists(pdf_directory):
                os.makedirs(pdf_directory)
            
            pdf_file_path = f"{pdf_directory}{self.invoice_number}.pdf"
            
            print(pdf_file_path)
            
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                                
                # Set the HTML content
                await page.set_content(html_content, wait_until='networkidle')
                
                # Generate PDF with options to fit content to a single page
                await page.pdf(
                    path=pdf_file_path,
                    format='A4',  # Or other formats like 'Letter'
                    print_background=True,
                    margin={'top': '10px', 'bottom': '10px', 'left': '10px', 'right': '10px'}
                )
                
                await browser.close()
                print(f"PDF successfully generated at {pdf_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_base64_image(self, image_path):
        """ Convert an image to a base64-encoded string """
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
        
    def generate_invoice_html(self):
        """ Generate HTML content for the invoice """
        invoice_number = str(self.invoice_number)
        invoice_date = self.calendar.selectedDate().toString('MMMM d, yyyy')
        venue = self.venue_input.text()
        client_name = self.client_name_input.text()
        phone_number = self.phone_number_input.text()
        bill_to = self.bill_to_input.text()
        
        # Generate item rows
        item_rows = ""
        total_amount = 0.0
        for row in range(self.item_table.rowCount()):
            item_name = self.item_table.item(row, 0).text()
            item_description = self.item_table.item(row, 1).text()
            rate = float(self.item_table.item(row, 2).text())
            quantity = float(self.item_table.item(row, 3).text())
            price = rate * quantity
            total_amount += price
            
            item_rows += f"""
            <tr>
                <td>{item_name}</td>
                <td>{item_description}</td>
                <td>{rate:.2f}</td>
                <td>{quantity}</td>
                <td>{price:.2f}</td>
            </tr>
            """
        
        amount_paid = 0.0  # or fetch from user input
        balance_due = total_amount - amount_paid
        
        # Fetch and encode the logo image
        logo_base64 = self.get_base64_image("logo.png")

        html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Invoice</title>
                <style>
                    * {{
                        border: 0;
                        box-sizing: content-box;
                        color: inherit;
                        font-family: inherit;
                        font-size: inherit;
                        font-style: inherit;
                        font-weight: inherit;
                        line-height: inherit;
                        list-style: none;
                        margin: 0;
                        padding: 0;
                        text-decoration: none;
                        vertical-align: top;
                    }}

                    address {{
                        display: flex;
                        flex-direction: row;
                        flex-wrap: wrap;
                        align-content: center;
                        justify-content: space-between;
                    }}
                    *[contenteditable] {{ border-radius: 0.25em; min-width: 1em; outline: 0; }}

                    *[contenteditable] {{ cursor: pointer; margin-bottom: 0; }}

                    *[contenteditable]:hover, *[contenteditable]:focus, td:hover *[contenteditable], td:focus *[contenteditable], img.hover {{ background: #DEF; box-shadow: 0 0 1em 0.5em #DEF; }}

                    span[contenteditable] {{ display: inline-block; }}

                    /* heading */

                    h1 {{ font: bold 100% sans-serif; letter-spacing: 0.5em; text-align: center; text-transform: uppercase; }}

                    /* table */

                    table {{ font-size: 75%; table-layout: fixed; width: 100%; }}
                    table {{ border-collapse: separate; border-spacing: 2px; }}
                    th, td {{ border-width: 1px; padding: 0.5em; position: relative; text-align: left; }}
                    th, td {{ border-radius: 0.25em; border-style: solid; }}
                    th {{ background: #EEE; border-color: #BBB; }}
                    td {{ border-color: #DDD; }}

                    /* page */

                    html {{ font: 16px/1 'Open Sans', sans-serif; overflow: auto; padding: 0.5in; }}
                    html {{ background: #999; cursor: default; }}

                    body {{ box-sizing: border-box; height: 11in; margin: 0 auto; overflow: hidden; padding: 0.5in; width: 8.5in; }}
                    body {{ background: #FFF; border-radius: 1px; box-shadow: 0 0 1in -0.25in rgba(0, 0, 0, 0.5); }}

                    /* header */

                    header {{ margin: 0 0 3em; }}
                    header:after {{ clear: both; content: ""; display: table; }}

                    header h1 {{ background: #000; border-radius: 0.25em; color: #FFF; margin: 0 0 1em; padding: 0.5em 0; }}
                    header address {{ float: left; font-size: 75%; font-style: normal; line-height: 1.25; margin: 0 1em 1em 0; }}
                    header address p {{ margin: 0 0 0.25em; }}
                    header span, header img {{ display: block; float: left; }}
                    header span {{ margin: 0 0 1em 1em; max-height: 25%; max-width: 60%; position: relative; }}
                    header img {{ max-height: 100%; max-width: 100%; }}
                    header input {{ cursor: pointer; -ms-filter:"progid:DXImageTransform.Microsoft.Alpha(Opacity=0)"; height: 100%; left: 0; opacity: 0; position: absolute; top: 0; width: 100%; }}

                    /* article */

                    article, article address, table.meta, table.inventory {{ margin: 0 0 3em; }}
                    article:after {{ clear: both; content: ""; display: table; }}
                    article h1 {{ clip: rect(0 0 0 0); position: absolute; }}

                    article address {{ float: left; font-size: 125%; font-weight: bold; margin: 0; }}
                    article address table {{ margin: 0 0 10px 0 !important; }}
                    article {{ margin-bottom: 15px; }}
                    
                    header {{ margin: 0 0 1.2em 0; }}

                    /* table meta & balance */

                    #meta1 {{
                        z-index: 9;
                        opacity: 1;
                    }}

                    .smeta td {{
                        width: 60%;
                    }}
                    .smeta {{
                        float: right;
                        width: 40%;
                    }}

                    table.meta, table.balance {{
                        float: right;
                        width: 40%;
                    }}
                    table.meta:after, table.balance:after {{ clear: both; content: ""; display: table; }}

                    /* table meta */

                    table.meta th {{
                        width: 58%;
                    }}
                    table.meta td {{ width: 60%; }}

                    /* table items */

                    table.inventory {{ clear: both; width: 100%; }}
                    table.inventory th {{ font-weight: bold; text-align: center; }}

                    table.inventory td:nth-child(1) {{ width: 26%; }}
                    table.inventory td:nth-child(2) {{ width: 38%; }}
                    table.inventory td:nth-child(3) {{ text-align: right; width: 12%; }}
                    table.inventory td:nth-child(4) {{ text-align: right; width: 12%; }}
                    table.inventory td:nth-child(5) {{ text-align: right; width: 12%; }}

                    /* table balance */

                    table.balance th, table.balance td {{ width: 50%; }}
                    table.balance td {{ text-align: right; }}

                    /* aside */

                    aside h1 {{ border: none; border-width: 0 0 1px; margin: 0 0 1em; }}
                    aside h1 {{ border-color: #999; border-bottom-style: solid; }}

                    /* javascript */

                    .add, .cut {{
                        border-width: 1px;
                        display: block;
                        font-size: .8rem;
                        padding: 0.25em 0.5em;	
                        float: left;
                        text-align: center;
                        width: 0.6em;
                    }}

                    .add, .cut {{
                        background: #9AF;
                        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
                        background-image: -moz-linear-gradient(#00ADEE 5%, #0078A5 100%);
                        background-image: -webkit-linear-gradient(#00ADEE 5%, #0078A5 100%);
                        border-radius: 0.5em;
                        border-color: #0076A3;
                        color: #FFF;
                        cursor: pointer;
                        font-weight: bold;
                        text-shadow: 0 -1px 2px rgba(0,0,0,0.333);
                    }}

                    .add {{ margin: -2.5em 0 0; }}

                    .add:hover {{ background: #00ADEE; }}

                    .cut {{ opacity: 0; position: absolute; top: 0; left: -1.5em; }}
                    .cut {{ -webkit-transition: opacity 100ms ease-in; }}

                    tr:hover .cut {{ opacity: 1; }}

                    @media print {{
                        * {{ -webkit-print-color-adjust: exact; }}
                        html {{ background: none; padding: 0; }}
                        body {{ box-shadow: none; margin: 0; }}
                        span:empty {{ display: none; }}
                        .add, .cut {{ display: none; }}
                    }}

                    @page {{ margin: 0; }}
                </style>
            </head>
            <body>
                <header>
                    <h1>Invoice</h1>
                    <img width="180" height="130" alt="Logo" src="data:image/png;base64,{logo_base64}">
                    <table class="smeta">
                        <tr>
                            <th>Invoice #</th>
                            <td>{invoice_number}</td>
                        </tr>
                        <tr>
                            <th>Date</th>
                            <td>{invoice_date}</td>
                        </tr>
                        <tr>
                            <th>Venue</th>
                            <td>{venue}</td>
                        </tr>
                    </table>
                </header>
                <article>
                    <h1>Recipient</h1>
                    <address>
                        <table class="meta" id="meta1">
                            <tr>
                                <th>Client Name</th>
                                <td>{client_name}</td>
                            </tr>
                            <tr>
                                <th>Phone Number</th>
                                <td>{phone_number}</td>
                            </tr>
                            <tr>
                                <th>Bill To</th>
                                <td>{bill_to}</td>
                            </tr>
                        </table>
                        <table class="meta" style="width: 50%;">
                            <tr>
                                <th style="width: 40%;"><span contenteditable>Bank</span></th>
                                <td><span contenteditable>HBL (Habib Bank Limited)</span></td>
                            </tr>
                            <tr>
                                <th style="width: 40%;"><span>Account Title</span></th>
                                <td><span>Rameez Ahmed</span></td>
                            </tr>
                            <tr>
                                <th style="width: 40%;"><span>Account Number</span></th>
                                <td><span></span><span>00207901029503</span></td>
                            </tr>
                        </table>
                    </address>
                    <section style="overflow: auto;border: 1px solid;">
                        <table class="inventory">
                            <thead>
                                <tr>
                                    <th>Item</th>
                                    <th>Description</th>
                                    <th>Rate</th>
                                    <th>Quantity</th>
                                    <th>Price</th>
                                </tr>
                            </thead>
                            <tbody>
                                {item_rows}
                            </tbody>
                        </table>
                        <table class="balance">
                            <tr>
                                <th>Total</th>
                                <td>{total_amount:.2f}</td>
                            </tr>
                            <tr>
                                <th>Amount Paid</th>
                                <td>{amount_paid:.2f}</td>
                            </tr>
                            <tr>
                                <th>Balance Due</th>
                                <td>{balance_due:.2f}</td>
                            </tr>
                        </table>
                    </section>
                </article>
                <aside>
                    <h1><span contenteditable>Additional Notes</span></h1>
                    <div contenteditable>
                        <p>
                        <h3 style="font-weight: 600;">Payment Terms:</h3><br />
                        <ul>
                            <li class="__lis"><span>A 50% advance will be given before the event, and the remaining
                                    payment will be cleared by the next day of the event. Otherwise, raw data will not be provided
                                    for selection.</span></li>
                        </ul><br />
                        <h3 style="font-weight: 600;">Terms and Conditions:</h3><br />
                        <ul>
                            <li class="__lis">No payment will be refunded in case of any mishap or unforeseen situation /
                                circumstances occurred.</li> <br />
                            <li class="__lis">Client can only provide the extended date of the event.</li> <br />
                            <li class="__lis">Misbehavior of client will not be accepted.</li> <br />
                            <li class="__lis">If photographer provides any suggestion / advice regarding event management and client
                                don't listen or take it seriously so it will be not our responsibility.</li><br />
                            <li class="__lis">Client Pictures will be used on our page regarding marketing purposes at Instagram and
                                Facebook.</li><br />
                            <li class="__lis">Ask for update on editing after 15 days of the event.</li><br />
                        </ul>
                        </p>
                        <p>Kindly read this E-mail and instructions carefully and reply back to this but E-mail for confirmation. If
                            any query so please contact us on:</p><br />

                        <div style="display: flex;
                        flex-direction: column;
                        flex-wrap: wrap;
                        align-content: flex-end;
                        margin-top: 10px;">
                            <div>
                                <h4 style="font-weight: 600; font-size: 1.1rem;">Thanks & Regards,</h4>
                            </div><br />
                            <span style="font-size: 1.1rem;">Team Rameezdesaiphotography</span>
                            .
                        </div>
                    </div>
                </aside>
            </body>
            </html>
            """
        return html_content


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InvoiceApp()
    window.show()
    sys.exit(app.exec_())
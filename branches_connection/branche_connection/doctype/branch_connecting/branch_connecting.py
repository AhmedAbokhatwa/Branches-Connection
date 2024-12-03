# Copyright (c) 2024, Ahmed Reda Abu-khatwa and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.frappeclient import FrappeClient

class BranchConnecting(Document):
    @frappe.whitelist()
    def create_connection(self):
        url_producer = self.url
        api_key = self.api_key
        api_secret = self.api_secret

        if not url_producer or not api_key or not api_secret:
            frappe.throw(_("Missing producer URL, API key, or API secret"))

        try:
            # Create a connection using the FrappeClient
            connection = FrappeClient(url=url_producer, api_key=api_key, api_secret=api_secret)

            # Check if the connection object is successfully created
            if connection:
                self.connection = "Connected"
            else:
                self.connection = "Disconnected"
        
        except Exception as e:
            self.connection = "Disconnected"
            frappe.log_error(message=str(e), title="Connection Error")

        # Return the status so it can be displayed in the frontend
        return self.connection

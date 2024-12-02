import frappe
from frappe.utils.data import get_url
from frappe.utils.password import get_decrypted_password
import json

@frappe.whitelist()
def create_consumer(doc):
    # Deserialize the JSON string into a dictionary
    if isinstance(doc, str):
        doc = json.loads(doc)

    # Create a new Event Consumer document
    consumer = frappe.new_doc("Event Consumer")

    # Convert the incoming data into a usable format
    data = get_request_data(doc)
    consumer.callback_url = data["event_consumer"]
    consumer.user = data.get("user")
    consumer.api_key = data.get("api_key")
    consumer.api_secret = data.get("api_secret")
    consumer.incoming_change = True

    # Add consumer doctypes with conditions
    consumer_doctypes = json.loads(data["consumer_doctypes"])
    for entry in consumer_doctypes:
        consumer.append(
            "consumer_doctypes",
            {
                "ref_doctype": entry.get("doctype"),
                "status": "Pending",
                "condition": entry.get("condition"),
            },
        )

    # Insert the new consumer document into the database
    consumer.insert(ignore_permissions=True)
    frappe.db.commit()

    frappe.msgprint("Event Consumer inserted successfully.")


@frappe.whitelist()
def get_request_data(doc):
    # Ensure `doc` is a dictionary (deserialized)
    if isinstance(doc, str):
        doc = json.loads(doc)

    consumer_doctypes = []
    for entry in doc.get("branch_doctypes", []):
        if entry.get("has_mapping"):
            # If there's a mapping, get the remote doctype from Document Type Mapping
            dt = frappe.db.get_value("Document Type Mapping", entry.get("mapping"), "remote_doctype")
        else:
            dt = entry.get("ref_doctype")
        consumer_doctypes.append({"doctype": dt, "condition": entry.get("condition")})

    # Fetch the user's API key and secret
    user_key = frappe.db.get_value("User", doc.get("user"), "api_key")
    user_secret = get_decrypted_password("User", doc.get("user"), "api_secret")

    return {
        "event_consumer": get_url(),
        "consumer_doctypes": json.dumps(consumer_doctypes),
        "user": doc.get("user"),
        "api_key": user_key,
        "api_secret": user_secret,
    }

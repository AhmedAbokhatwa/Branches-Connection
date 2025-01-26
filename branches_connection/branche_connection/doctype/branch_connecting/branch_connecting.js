// Copyright (c) 2024, Ahmed Reda Abu-khatwa and contributors
// For license information, please see license.txt
frappe.ui.form.on("Branch Connecting", {
  refresh(frm) {
      // Add a custom button to initiate connection
      frm.add_custom_button("Create Connection", () => {
          frm.call({
              method: "create_connection",
              doc: frm.doc, // Automatically sends the current document context
              callback: function (res) {
                  if (res && res.message) {
                      frappe.msgprint(__("Connection Status: " + res.message));
                      frm.set_value("connection", res.message); // Dynamically update the status on form
                      frm.refresh_field("connection");
                  }
              }
          });
      });
  },
});
////////////////////////////////////////////indictor for list view//////////////////////////
////////////////////////////////////////////indictor for list view//////////////////////////
////////////////////////////////////////////indictor for list view//////////////////////////
frappe.listview_settings['Branch Connecting'] = {
  get_indicator(doc) {
      // Customize indicator color for each connection
      if (doc.connection == "Connected") {
          return [__("Connected"), "blue", "connection,=,Connected"];
      } else if (doc.connection == "DisConnected") {
          return [__("DisConnected"), "red", "connection,=,DisConnected"];
      }
  
  },
};

frappe.ui.form.on("Global Defaults", {
    refresh: function(frm) {
        // Enable/disable the sentence case field based on enable_change_case checkbox
        frm.toggle_enable("sentence_case", frm.doc.enable_change_case);
        
        // Add custom buttons for Change Case functionality
        if (frm.doc.enable_change_case) {
            // Preview Case button
            frm.add_custom_button(__("Preview Case"), function() {
                if (!frm.doc.sentence_case) {
                    frappe.msgprint({
                        title: __("Warning"),
                        message: __("Please select a Case Style first"),
                        indicator: "orange"
                    });
                    return;
                }
                
                frappe.prompt([
                    {
                        fieldname: "test_text",
                        fieldtype: "Small Text",
                        label: __("Text to Transform"),
                        reqd: 1,
                        default: "this is a test sentence. here is another sentence."
                    }
                ], function(values) {
                    frappe.call({
                        method: "change_case_pro.change_case.preview_case_change",
                        args: {
                            text: values.test_text,
                            style: frm.doc.sentence_case
                        },
                        callback: function(r) {
                            if (r.message) {
                                frappe.msgprint({
                                    title: __("Transformed Text"),
                                    message: `<div style="font-family: monospace;">
                                        <strong>Original:</strong><br>
                                        <div style="background: #f8f9fa; padding: 8px; margin: 4px 0; border-radius: 3px;">${values.test_text}</div>
                                        <strong>Transformed:</strong><br>
                                        <div style="background: #e7f3ff; padding: 8px; margin: 4px 0; border-radius: 3px; color: #0066cc;">${r.message}</div>
                                    </div>`,
                                    indicator: "green"
                                });
                            }
                        }
                    });
                }, __("Test Case Transformation"), __("Transform"));
            }, __("Change Case"));
            
            // Test Installation button
            frm.add_custom_button(__("Test Installation"), function() {
                frappe.call({
                    method: "change_case_pro.change_case.test_installation",
                    callback: function(r) {
                        if (r.message) {
                            let status = r.message;
                            let indicator = status.status === "success" ? "green" : status.status === "error" ? "red" : "orange";
                            
                            let message = `<div style="font-family: monospace;">
                                <strong>Installation Status:</strong><br>
                                • Custom Fields: ${status.custom_fields_exist ? '✓' : '✗'}<br>
                                • Transformation: ${status.transformation_works ? '✓' : '✗'}<br>
                                • Hooks: ${status.hooks_registered ? '✓' : '✗'}<br><br>
                                <strong>Overall Status: ${status.status.toUpperCase()}</strong>
                            </div>`;
                            
                            if (status.error) {
                                message += `<br><strong>Error:</strong> ${status.error}`;
                            }
                            
                            frappe.msgprint({
                                title: __("Installation Test Results"),
                                message: message,
                                indicator: indicator
                            });
                        }
                    }
                });
            }, __("Change Case"));
        }
    },

    enable_change_case: function(frm) {
        // Toggle the sentence_case field when enable_change_case is changed
        frm.toggle_enable("sentence_case", frm.doc.enable_change_case);
        
        // Clear sentence_case if change case is disabled
        if (!frm.doc.enable_change_case) {
            frm.set_value("sentence_case", "");
        }
        
        // Show status message
        if (frm.doc.enable_change_case) {
            frappe.show_alert({
                message: __('Change Case enabled! Select a case style below.'),
                indicator: 'green'
            }, 3);
        } else {
            frappe.show_alert({
                message: __('Change Case disabled.'),
                indicator: 'orange'
            }, 3);
        }
        
        // Refresh to show/hide buttons
        frm.refresh();
    },

    sentence_case: function(frm) {
        // Show a message when case style is selected
        if (frm.doc.sentence_case && frm.doc.enable_change_case) {
            frappe.show_alert({
                message: __(`Case transformation set to: ${frm.doc.sentence_case}`),
                indicator: 'green'
            }, 3);
        }
    }
});
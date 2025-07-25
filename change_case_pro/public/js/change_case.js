frappe.ui.form.on("Global Defaults", {
    refresh: function(frm) {
        // Enable/disable the sentence case field based on enable_change_case checkbox
        frm.toggle_enable("sentence_case", frm.doc.enable_change_case);
        
        // Add custom button to preview case transformation
        if (frm.doc.enable_change_case) {
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
                        method: "change_case.events.preview_case_change",
                        args: {
                            text: values.test_text,
                            style: frm.doc.sentence_case
                        },
                        callback: function(r) {
                            if (r.message) {
                                frappe.msgprint({
                                    title: __("Transformed Text"),
                                    message: `<strong>Original:</strong> ${values.test_text}<br><br><strong>Transformed:</strong> ${r.message}`,
                                    indicator: "green"
                                });
                            }
                        }
                    });
                }, __("Test Case Transformation"), __("Transform"));
            }, __("Actions"));
        }
    },

    enable_change_case: function(frm) {
        // Toggle the sentence_case field when enable_change_case is changed
        frm.toggle_enable("sentence_case", frm.doc.enable_change_case);
        
        // Clear sentence_case if change case is disabled
        if (!frm.doc.enable_change_case) {
            frm.set_value("sentence_case", "");
        }
        
        // Refresh to show/hide the Preview button
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
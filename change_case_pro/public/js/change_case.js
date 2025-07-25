frappe.ui.form.on("Global Defaults", {
    refresh: function(frm) {
        // Enable/disable the sentence case field based on enable_change_case checkbox
        frm.toggle_enable("sentence_case", frm.doc.enable_change_case);
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
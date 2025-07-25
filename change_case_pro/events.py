def create_custom_fields():
    """Create custom fields in Global Defaults"""
    print("📝 Creating custom fields in Global Defaults...")
    
    custom_fields = [
        {
            "doctype": "Custom Field",
            "dt": "Global Defaults", 
            "fieldname": "change_case_section",
            "label": "Change Case Settings",
            "fieldtype": "Section Break",
            "insert_after": "default_company",
            "collapsible": 0
        },
        {
            "doctype": "Custom Field",
            "dt": "Global Defaults",
            "fieldname": "enable_change_case", 
            "label": "Enable Change Case",
            "fieldtype": "Check",
            "insert_after": "change_case_section",
            "description": "Enable automatic case transformation for all text fields across the system",
            "default": "0"
        },
        {
            "doctype": "Custom Field",
            "dt": "Global Defaults", 
            "fieldname": "sentence_case",
            "label": "Case Style",
            "fieldtype": "Select",
            "options": "Sentence case\nlowercase\nUPPERCASE\nCapitalize Each Word\ntOGGLE cASE\ncamelCase\nPascalCase",
            "insert_after": "enable_change_case",
            "depends_on": "eval:doc.enable_change_case",
            "description": "Select the case transformation style to apply globally",
            "default": "Sentence case"
        }
    ]
    
    fields_created = 0
    for field_data in custom_fields:
        try:
            # Check if field already exists
            existing_field = frappe.db.exists("Custom Field", {
                "dt": field_data["dt"], 
                "fieldname": field_data["fieldname"]
            })
            
            if not existing_field:
                custom_field = frappe.get_doc(field_data)
                custom_field.insert(ignore_permissions=True)
                frappe.db.commit()
                fields_created += 1
                print(f"   ✅ Created custom field: {field_data['fieldname']}")
            else:
                print(f"   ℹ️  Custom field already exists: {field_data['fieldname']}")
                
        except Exception as e:
            print(f"   ❌ Error creating custom field {field_data['fieldname']}: {str(e)}")
            frappe.log_error(f"Custom field creation error: {str(e)}", "Change Case Install")
    
    if fields_created > 0:
        print(f"📝 Created {fields_created} new custom fields")
    else:
        print("📝 All custom fields already exist")
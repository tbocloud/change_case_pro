# change_case.py
import frappe

def change_case(text, style):
    """Transform text based on the specified case style."""
    if not text or not isinstance(text, str) or not text.strip():
        return text

    try:
        if style == "Sentence case":
            # Capitalize first letter of each sentence
            sentences = text.split('. ')
            result = []
            for sentence in sentences:
                if sentence.strip():
                    cleaned = sentence.strip()
                    if len(cleaned) > 1:
                        result.append(cleaned[0].upper() + cleaned[1:].lower())
                    else:
                        result.append(cleaned.upper())
                else:
                    result.append(sentence)
            return '. '.join(result)
        elif style == "lowercase":
            return text.lower()
        elif style == "UPPERCASE":
            return text.upper()
        elif style == "Capitalize Each Word":
            return text.title()
        elif style == "tOGGLE cASE":
            return ''.join(c.lower() if c.isupper() else c.upper() for c in text)
        elif style == "camelCase":
            words = text.split()
            if not words:
                return text
            return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
        elif style == "PascalCase":
            return ''.join(word.capitalize() for word in text.split())
    except Exception as e:
        frappe.log_error(f"Change Case Transformation Error: {str(e)}", "Change Case")
        return text

    return text

@frappe.whitelist()
def preview_case_change(text, style):
    """Preview case transformation - called from JavaScript"""
    return change_case(text, style)

def apply_global_case(doc, method):
    """Apply case transformation to eligible fields before saving a document - WORKS GLOBALLY."""
    try:
        # Skip Global Defaults to prevent recursion
        if doc.doctype == "Global Defaults":
            return
            
        # Get Global Defaults settings with better error handling
        try:
            defaults = frappe.get_single("Global Defaults")
        except Exception:
            return
            
        # Check if change case is enabled
        enable_change_case = getattr(defaults, "enable_change_case", 0)
        if not enable_change_case or enable_change_case == 0:
            return

        case_style = getattr(defaults, "sentence_case", None)
        if not case_style or case_style == "":
            return

        # Skip only critical system doctypes that could break the system
        critical_system_doctypes = [
            "DocType", "DocField", "DocPerm", "Custom Field", "Custom Script", 
            "Property Setter", "Print Format", "Server Script", "Client Script",
            "Error Log", "Activity Log", "Version", "File", "Email Queue",
            "Communication", "Comment", "View Log", "Access Log", "Route History",
            "Global Defaults", "User", "Role", "System Settings"
        ]
        if doc.doctype in critical_system_doctypes:
            return

        # Get document meta to identify text fields
        from frappe.model.meta import get_meta
        try:
            meta = get_meta(doc.doctype)
        except Exception:
            return

        # Transform ALL eligible text fields globally
        fields_transformed = 0
        for field in meta.fields:
            # Include all text-based fieldtypes
            if field.fieldtype in ["Data", "Small Text", "Text", "Text Editor", "Long Text", "Markdown Editor"]:
                try:
                    field_value = getattr(doc, field.fieldname, None)
                    if isinstance(field_value, str) and field_value.strip():
                        # Skip only essential system fields
                        skip_fields = [
                            "name", "owner", "modified_by", "creation", "modified", 
                            "docstatus", "idx", "parent", "parentfield", "parenttype",
                            "_user_tags", "_comments", "_assign", "_liked_by", "route"
                        ]
                        if field.fieldname not in skip_fields and not field.fieldname.startswith('_'):
                            original_value = field_value
                            transformed_value = change_case(field_value, case_style)
                            if original_value != transformed_value:
                                setattr(doc, field.fieldname, transformed_value)
                                fields_transformed += 1
                except Exception as field_error:
                    # Don't let field errors break the save
                    continue

        # Optional: Log successful transformation for debugging
        if fields_transformed > 0:
            print(f"✓ Applied case transformation to {fields_transformed} fields in {doc.doctype}")

    except Exception as e:
        # Don't raise the exception to avoid breaking the save process
        print(f"Case Transform Error in {doc.doctype}: {str(e)}")
        pass

# Installation Functions
def after_install():
    """Setup custom fields after app installation"""
    try:
        print("\n" + "="*50)
        print("🚀 SETTING UP CHANGE CASE PRO APP")
        print("="*50)
        
        create_custom_fields()
        setup_global_defaults()
        
        frappe.db.commit()
        frappe.clear_cache()
        
        print("✅ Change Case Pro app setup completed successfully!")
        print("📍 Go to Global Defaults to enable Change Case")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"❌ Setup error: {str(e)}")
        frappe.log_error(f"Change Case installation error: {str(e)}", "Change Case Install")

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
            "insert_after": "default_distance_unit",
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

def setup_global_defaults():
    """Initialize Global Defaults with Change Case settings"""
    try:
        print("⚙️  Initializing Global Defaults...")
        defaults = frappe.get_single("Global Defaults")
        
        # Only set defaults if fields exist and aren't already set
        if hasattr(defaults, "enable_change_case") and not defaults.enable_change_case:
            defaults.enable_change_case = 0  # Start disabled
            
        if hasattr(defaults, "sentence_case") and not defaults.sentence_case:
            defaults.sentence_case = "Sentence case"  # Default style
            
        defaults.save(ignore_permissions=True)
        frappe.db.commit()
        print("   ✅ Global Defaults initialized")
        
    except Exception as e:
        print(f"   ⚠️  Could not initialize Global Defaults: {str(e)}")
        # Don't fail installation if this doesn't work

def before_uninstall():
    """Clean up custom fields before app uninstallation"""
    try:
        print("🧹 Cleaning up Change Case Pro app...")
        # Remove custom fields
        custom_fields = frappe.get_all("Custom Field", 
            filters={"dt": "Global Defaults", "fieldname": ["in", ["enable_change_case", "sentence_case", "change_case_section"]]})
        
        for field in custom_fields:
            frappe.delete_doc("Custom Field", field.name, ignore_permissions=True)
            print(f"✅ Removed custom field: {field.name}")
            
        frappe.db.commit()
        print("✅ Change Case custom fields removed successfully")
    except Exception as e:
        print(f"❌ Error removing custom fields: {str(e)}")
        frappe.log_error(f"Custom field removal error: {str(e)}", "Change Case Uninstall")

@frappe.whitelist()
def test_installation():
    """Test if the installation is working correctly"""
    try:
        # Test 1: Check if custom fields exist
        defaults = frappe.get_single("Global Defaults")
        has_enable = hasattr(defaults, "enable_change_case")
        has_style = hasattr(defaults, "sentence_case")
        
        # Test 2: Test transformation function
        test_result = change_case("hello world", "UPPERCASE")
        
        # Test 3: Check hooks
        hooks = frappe.get_hooks()
        hook_exists = "change_case_pro.change_case.apply_global_case" in hooks.get("before_save", [])
        
        return {
            "custom_fields_exist": has_enable and has_style,
            "transformation_works": test_result == "HELLO WORLD",
            "hooks_registered": hook_exists,
            "status": "success" if (has_enable and has_style and test_result == "HELLO WORLD" and hook_exists) else "partial"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }
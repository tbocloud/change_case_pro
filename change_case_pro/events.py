# events.py
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
                    result.append(sentence.strip()[0].upper() + sentence.strip()[1:].lower() if len(sentence.strip()) > 1 else sentence.strip().upper())
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
            "Global Defaults"  # Extra safety
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
                            "_user_tags", "_comments", "_assign", "_liked_by"
                        ]
                        if field.fieldname not in skip_fields and not field.fieldname.startswith('_'):
                            original_value = field_value
                            transformed_value = change_case(field_value, case_style)
                            if original_value != transformed_value:
                                setattr(doc, field.fieldname, transformed_value)
                                fields_transformed += 1
                                # Debug log for verification
                                frappe.logger().info(f"CASE TRANSFORM: {doc.doctype}.{field.fieldname}: '{original_value}' -> '{transformed_value}'")
                except Exception as field_error:
                    frappe.logger().error(f"Field transformation error {doc.doctype}.{field.fieldname}: {str(field_error)}")
                    continue

        # Log successful transformation
        if fields_transformed > 0:
            frappe.logger().info(f"Applied case transformation to {fields_transformed} fields in {doc.doctype} {getattr(doc, 'name', 'NEW')}")

    except Exception as e:
        frappe.logger().error(f"Global Case Transform Error in {doc.doctype}: {str(e)}")
        # Don't raise the exception to avoid breaking the save process
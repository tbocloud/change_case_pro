# Change Case - Global Text Transformation for Frappe

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Frappe](https://img.shields.io/badge/Frappe-Framework-blue.svg)](https://frappeframework.com)

A powerful Frappe app that automatically transforms text case across your entire Frappe/ERPNext system based on global settings.

## 🚀 Features

- **Global Text Transformation**: Automatically converts text in ALL documents across your Frappe site
- **Multiple Case Styles**: 7 different transformation options
- **Easy Control**: Enable/disable from Global Defaults with one click
- **Smart Filtering**: Safely skips system doctypes to prevent conflicts
- **Real-time Preview**: Test transformations before applying
- **Works Everywhere**: Customer, Item, Sales Invoice, Purchase Order, and all custom doctypes

## 📋 Supported Case Styles

| Style | Example |
|-------|---------|
| **Sentence case** | `Hello world. This is second sentence.` |
| **lowercase** | `hello world` |
| **UPPERCASE** | `HELLO WORLD` |
| **Capitalize Each Word** | `Hello World` |
| **tOGGLE cASE** | `hELLO wORLD` |
| **camelCase** | `helloWorld` |
| **PascalCase** | `HelloWorld` |

## 🛠️ Installation

### Prerequisites
- Frappe Framework v13+ or ERPNext
- Python 3.6+

### Install Steps

1. **Navigate to your bench directory**
   ```bash
   cd /path/to/your/bench
   ```

2. **Download the app**
   ```bash
   bench get-app https://github.com/tbocloud/change_case_pro.git
   ```

3. **Install on your site**
   ```bash
   bench --site your-site-name install-app change_case_pro
   ```

4. **Restart and clear cache**
   ```bash
   bench restart
   bench clear-cache
   ```

## 🎯 Usage

### Quick Setup
1. **Go to Global Defaults** in your Frappe desk
2. **Check "Enable Change Case"** ✅
3. **Select your preferred Case Style** (e.g., "UPPERCASE")
4. **Save the settings**

### That's it! 
Now every text field in every document will automatically transform based on your settings when saved.

### Example
**Before enabling Change Case:**
- Customer Name: `john smith enterprises`

**After enabling "UPPERCASE" style:**
- Customer Name: `JOHN SMITH ENTERPRISES` ✨

### Preview Transformations
Use the **"Preview Case"** button in Global Defaults to test how text will be transformed before applying it system-wide.

## 🔧 Configuration

### Global Defaults Fields Added

The app automatically adds these fields to your Global Defaults:

| Field | Type | Description |
|-------|------|-------------|
| **Enable Change Case** | Check | Master switch to enable/disable case transformation |
| **Case Style** | Select | Choose from 7 different case transformation styles |

### Affected Field Types

The transformation applies to these field types:
- Data
- Small Text  
- Text
- Text Editor
- Long Text
- Markdown Editor

### Protected Fields

These fields are automatically skipped to maintain system integrity:
- System fields (`name`, `owner`, `modified_by`, etc.)
- Critical doctypes (DocType, Custom Field, etc.)
- Fields starting with underscore (`_user_tags`, etc.)

## 🧪 Testing

### Test in Console
```python
# Test the transformation function
from change_case.events import change_case
result = change_case("hello world", "UPPERCASE")
print(result)  # Output: HELLO WORLD
```

### Test with Live Documents
1. Create a new Customer with lowercase name
2. Save the document
3. Verify the name is transformed according to your Global Defaults setting

## 📁 File Structure

```
change_case/
├── hooks.py                 # App configuration and hook registration
├── events.py               # Core transformation logic
├── install.py              # Installation and setup scripts
├── change_case.js          # Frontend JavaScript for Global Defaults
├── patches.py              # Utility functions for troubleshooting
└── README.md               # This documentation
```

## 🔍 Troubleshooting

### Case transformation not working?

1. **Check if enabled**:
   ```python
   defaults = frappe.get_single("Global Defaults")
   print(f"Enabled: {defaults.enable_change_case}")
   print(f"Style: {defaults.sentence_case}")
   ```

2. **Verify hooks are registered**:
   ```python
   hooks = frappe.get_hooks()
   print("change_case.events.apply_global_case" in hooks.get("before_save", []))
   ```

3. **Restart bench**:
   ```bash
   bench restart
   bench clear-cache
   ```

### Manual field creation (if needed)
If custom fields aren't created automatically, run:
```python
from change_case.install import create_custom_fields
create_custom_fields()
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/tbocloud/change_case_pro/issues))
- **Email**: sammish.thundiyil@gmail.com

## 🙏 Acknowledgments

- Built for the Frappe Framework community
- Inspired by the need for consistent text formatting across business documents
- Thanks to all contributors and testers

---

**Made with ❤️ for the Frappe community**

⭐ **Star this repo if it helped you!**

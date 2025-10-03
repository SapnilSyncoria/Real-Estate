"# Real-Estate" 
"# Real-Estate" 
Real Estate Bipro — Odoo Customization Suite

This project is a comprehensive Odoo application for real-estate management, enriched with customizations in sales, invoicing, accounting, products, and security.
It is inspired by the concepts in Odoo’s Server Framework 101 (15 chapters) and extends beyond the tutorial, delivering a production-ready system.

Modules
Real_Estate_Bipro — Core real-estate module: properties, units, tenants, leases/contracts.
estate_account — Accounting integration for property income, journals, and custom postings.
invoice_modification — Extended invoice functionality with custom fields and logic.
invoice_to_sell — Seamless linkage between invoices and sales orders.
product_modification — Product template adjustments to represent properties as products.
Key Features
Property & Unit Management: End-to-end property, unit, and contract handling.
Lease & Tenancy Contracts: Rent terms, schedules, deposits, start/end dates, and validations.
Sales Integration: Extended sale.order with property-related fields and workflows.
Invoice Enhancements:
Extra custom fields in invoice lines.
Discount handling and total discount calculations.
Invoice-to-sale linkage for better traceability.
Accounting Extensions: Automated posting to appropriate journals and accounts.
Product Customization: Support for treating real-estate assets as products in Odoo.
Security Layer:
Role-based access rights.
Record rules (ir.rules) for data isolation.
Granular permission control across models.
Development Principles
Modular architecture: Core logic and supporting features split into independent add-ons.
ORM best practices: Declarative fields, relational links, computed values, and constraints.
Inheritance-driven: Extension of core Odoo models (sale.order, account.move, product.template) instead of overrides.
Business rules enforcement: Constraints for dates, contract overlaps, and data integrity.
User experience focus: Custom views, buttons, menus, and improved workflows.
Beyond tutorial scope: Advanced features such as invoice modifications, discount management, security policies, and financial integration.
Author

Developed by Sapnil Sarker Bipro.

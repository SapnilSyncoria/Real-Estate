{
    'name': "Invoice Modification",
    'version': '1.0',
    'depends': ['account'],
    'author': "Sapnil",
    'category': 'Accounting',
    'summary': "Custom modifications for invoice model",
    'description': """Create a link in the invoice which directs to the main property record.""",
    'data': [
        'views/invoice_modification.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

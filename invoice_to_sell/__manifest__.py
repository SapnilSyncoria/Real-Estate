{
    'name': "Invoice to Sell",
    'version': '1.0',
    'depends': ['account', 'sale', 'web'],
    'author': "Sapnil",
    'category': 'Accounting',
    'summary': "Custom modifications for invoice model",
    'description': """Create a link in the invoice which will create the new sell order for that invoice.""",
    'data': [
        'views/invoice_to_cell.xml',
        'views/cell_to_invoice_views.xml',
        'views/sale_order_line_discount_views.xml',
        'views/sale_order_line_discount_views_2.xml',

    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}

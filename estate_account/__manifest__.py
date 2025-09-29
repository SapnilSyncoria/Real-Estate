{
    'name': 'Estate Account',
    'version': '1.0',
    'summary': 'Link module between Estate and Accounting',
    'description': 'A module to connect Real Estate with Accounting.',
    'category': 'Accounting',
    'author': 'Sapnil',
    'depends': ['Real_estate_bipro', 'account'],  # Depends on estate and account
    'data': [
        'views/estate_property.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

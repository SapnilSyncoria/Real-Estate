{
    'name': "Real Estate Bipro",
    'version': '1.0',
    'author': "Sapnil Sarker Bipro",
    'category': 'Custom',
    'summary': "I am going to modify it from scratch",


    'depends': ['base'],   # no dependencies
    'data': ['security/ir.model.access.csv','views/estate_property_types.xml',
             'views/estate_property_tags.xml',
             'views/estate_property_views.xml',
            'views/estate_property_offers.xml',
              'views/estate_menus.xml',
            'views/res_user.xml',
             'security/real_estate_security.xml',
             # 'security/real_estate_security_2.xml'

    ],


    'installable': True,
    'application': True,   # <- this makes it show up in Apps menu
    'auto_install': False,
    'license': 'LGPL-3',
}

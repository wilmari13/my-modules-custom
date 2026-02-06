# -*- coding: utf-8 -*-
{
    'name': "account_discount_policy",

    'summary': "Implement automatic discount rules on invoices based on customer type (Retail, Wholesale, VIP).",

    'description': """
Long description of module's purpose
    """,

    'author': "Wilmari Padrino",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv', 
        'data/client_type.xml',     
        'views/discount_policy_views.xml',   
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


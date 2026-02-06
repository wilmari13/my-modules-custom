# -*- coding: utf-8 -*-
{
    'name': "smart_storage_tags",

    'summary': "Automatic generation of notifications and dashboard of products with stock below the minimum threshold.",

    'description': """
Long description of module's purpose
    """,

    'author': "Wilmari Padrino",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/manage_tags_wizard_views.xml',
        'views/product_template_views.xml',
        'views/storage_tag_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


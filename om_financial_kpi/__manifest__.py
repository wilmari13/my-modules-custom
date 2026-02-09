# -*- coding: utf-8 -*-
{
    'name': "om_financial_kpi",

    'summary': "financial indicator dashboard based on accounting formulas.",

    'description': """
Long description of module's purpose
    """,

    'author': "Wilmari Padrino",
    'website': "https://www.yourcompany.com",

    
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_financial_kpi.xml',
        'data/kpi_data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


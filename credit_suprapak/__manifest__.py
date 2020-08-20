# -*- coding: utf-8 -*-
{
    'name': "Credit limit Suprapak",

    'summary': "Credit limit Suprapak",

    'description': "Credit limit Suprapak",

    'author': "Todoo SAS",
    'contributors': "Pablo Arcos pa@todoo,co",
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Generic Modules/Accounting',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['dev_customer_credit_limit'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/templates.xml',
        'wizard/customer_limit_wizard.xml',
        'data/mail_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

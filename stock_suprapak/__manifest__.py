# -*- coding: utf-8 -*-
{
    'name': "Suprapak stock",

    'summary': "Stock suprapak",

    'description': "Stock suprapak",

    'author': "Todoo SAS",
    'contributors': "Jonathan Leon jl@todoo,co",
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Operations',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['stock','sale_management','hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_template_view.xml',
        'views/stock_picking_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

# -*- coding: utf-8 -*-
{
    'name': "OTIF Suprapak",

    'summary': "",

    'description': "This is a module for Suprapak",

    'author': "Todoo",
    'website': "http://www.todoo.co",
    'contributors': "Livingston Arias la@todoo,co",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Contacts',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_management','mrp'],

    # always loaded
    'data': [
         # 'views/sale_suprapak.xml',
         'views/res_country_state.xml',
         'views/sale_order_view.xml',
         'views/res_partner_view.xml',
         'wizard/view_wizard_otif.xml',
    ],
    # only loaded in demonstration mode
    'images': [],
    'application': True,
}
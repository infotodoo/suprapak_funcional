# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Suprapak",

    'summary': "",

    'description': "This is a changes for Suprapak",

    'author': "Todoo",
    'website': "http://www.todoo.co",
    'contributors': "Livingston Arias la@todoo,co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Helpdesk',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['helpdesk'],

    # always loaded
    'data': [
        #'views/view_helpdesk.xml',
        #'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    #'images': ['static/description/icon.png'],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
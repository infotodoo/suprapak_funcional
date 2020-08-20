# -*- coding: utf-8 -*-
{
    'name': "Maintenance Suprapak",

    'summary': "Maintenance Suprapak",

    'description': "Maintenance Suprapak",

    'author': "Todoo SAS",
    'contributors': ['Carlos Guio fg@todo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Operations',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['maintenance'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_request_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

# -*- coding: utf-8 -*-
{
    'name': "CRM Suprapak",

    'summary': "CRM Suprapak",

    'description': "CRM Suprapak",

    'author': "Todoo SAS",
    'contributors': ['Pablo Arcos pa@todoo.co', 'Livingston Arias la@todoo,co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/CRM',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['crm', 'helpdesk'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'views/contacts_suprapak.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

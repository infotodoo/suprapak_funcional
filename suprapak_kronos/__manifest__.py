# -*- coding: utf-8 -*-
{
    'name': "Kronos",

    'summary': "",

    'description': "This is a module for Suprapak",

    'author': "Todoo",
    'website': "http://www.todoo.co",
    'contributors': "Livingston Arias la@todoo,co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_crm', 'mrp', 'stock_suprapak', 'base_address_city','sale_suprapak','stock'],

    # always loaded
    'data': [
        'mail_templates/wizard_create_quotation.xml',
        'mail_templates/wizard_revision.xml',
        'mail_templates/wizard_technical.xml',
        'mail_templates/wizard_design.xml',
        'mail_templates/wizard_approved.xml',
        'mail_templates/wizard_rejected.xml',
        'mail_templates/wizard_rejected_t.xml',
        'mail_templates/wizard_rejected_d.xml',
        'mail_templates/wizard_pantone_view.xml',
        'views/res_partner_view.xml',
        'views/templates.xml',
        'report/report_sale_supra.xml',
        'report/report_sale_template_supra.xml',
        'views/data_sheet_view.xml',
        'views/data_sheet_menu.xml',
        'views/crm_lead_view.xml',
        'views/sale_order_view.xml',
        'security/ir.model.access.csv',
        'views/sale_template.xml',
        'views/stock_picking_view.xml',
        'views/mrp_production_view.xml',

    ],
    # only loaded in demonstration mode
    'images': ['static/description/icon.png'],
    'application': True,
}

# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale and inventory Comment',
    'version': '13.0.1.0.0',
    'author': 'MPTechnolabs',
    'maintainer': 'Sale and inventory Comment in sale order',
    'depends': ['sale_management', 'stock'],
    'summary': 'Sale and inventory Comment in sale order',
    'website': 'http://www.mptechnolabs.com',
    'category': 'Sale',
    'data': [
        'ir.model.access.csv',
        'views/sale_inventory_comment.xml',
    ],
    'installable': True,
    'auto_install': False,
}

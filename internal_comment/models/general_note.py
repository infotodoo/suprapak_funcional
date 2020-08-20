# -*- coding: utf-8 -*-
from odoo import api, fields, models
import datetime


class SaleNote(models.Model):
    _name = 'sale.note'

    name = fields.Char('Sale Note')
    note_date = fields.Datetime('Time', default=datetime.datetime.now())
    sale_order_id = fields.Many2one('sale.order', 'Order Id')
    type = fields.Selection([('sale', 'Sale'), ('warehouse', 'Warehouse')], 'Note Type')


# -*- coding: utf-8 -*-
from odoo import fields, models,http,_


class SaleQuatation(models.Model):
    _inherit = "sale.order"

    sale_note_ids = fields.Many2many('sale.note',string = 'Sale Note')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_note_ids = fields.Many2many(string='Send by Post', related='sale_id.sale_note_ids', readonly=False)

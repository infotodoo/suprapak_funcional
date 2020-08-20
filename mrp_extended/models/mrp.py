# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.tools import mute_logger
from odoo.exceptions import Warning


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    workorder_product_id = fields.Many2one('mrp.workorder')


class WorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    state = fields.Selection(selection_add=[('partial_done', 'Partially Done')])
    bom_id = fields.Many2one(
        string='BOM',
        comodel_name='mrp.bom',
        related='production_id.bom_id')  # store not needed default True
    component_product_id = fields.One2many(
        string='Materials',
        comodel_name='mrp.bom.line', related='bom_id.bom_line_ids')

    @api.model
    def _extract_bom_line(self, vals):
        return vals.pop('bom_line_ids', {})

    def _prepare_bom_vals(self, vals):
        self.ensure_one()
        return {
            'workorder_product_id': self.id,
            'bom_line_ids': vals,
        }

    def _process_bom_vals(self, vals):
        for record in self:
            if record.bom_ids:
                record.bom_ids[0].write({'bom_line_ids': vals})
            else:
                record.env['mrp.bom'].create(self._prepare_bom_vals(vals))


class Production(models.Model):
    _inherit = 'mrp.production'

    state = fields.Selection(selection_add=[('partial_done', 'Partially Done')])


class StockMove(models.Model):
    _inherit = 'stock.move.line'

    move_done = fields.Boolean('move done')

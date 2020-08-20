# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MrpSplit(models.Model):
    _inherit = 'mrp.workorder'

    def split_mo(self):
        product_qty = self.production_id.product_qty
        qty_producing = self.qty_producing
        if qty_producing < product_qty:
            self.env['change.production.qty'].create({
                'mo_id': self.production_id.id,
                'product_qty': product_qty - qty_producing,
            }).change_prod_qty()
            created_mo = self.env['mrp.production'].create({
                'name': self.production_id.name + '.1',
                'product_id': self.production_id.product_id.id,
                'bom_id': self.production_id.bom_id.id,
                'routing_id': self.production_id.routing_id.id,
                'product_uom_id': self.production_id.product_uom_id.id,
                'product_qty': qty_producing,
                'origin': self.production_id.name, })
            created_mo._onchange_move_raw()
            created_mo.button_plan()
        else:
            raise UserError(_('Please Enter Valid Quantity !'))

        return

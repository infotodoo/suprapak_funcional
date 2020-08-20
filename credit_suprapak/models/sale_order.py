# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _default_users_ids(self):
        group_id = self.env.ref('dev_customer_credit_limit.credit_limit_config')
        if group_id:
            return group_id.users
        else:
            return False

    users_ids = fields.Many2many('res.users', 'order_users_rel', 'order_id', 'users_id', 'Users', default=_default_users_ids)
    patrners_ids = fields.Many2many('res.partner', 'order_partner_rel', 'order_id', 'partner_id', 'Partners', compute='_compute_partners_ids')

    @api.depends('users_ids')
    def _compute_partners_ids(self):
        for record in self:
            record.patrners_ids = record.users_ids.partner_id if record.users_ids else False

    def compute_patrners_ids(self):
        partners = ''
        count = 0
        for partner in self.patrners_ids:
            count += 1
            if count == 1:
                partners += str(partner.id)
            else:
                partners += ', ' + str(partner.id)
        return partners

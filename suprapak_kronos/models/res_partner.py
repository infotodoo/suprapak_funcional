# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResSector(models.Model):
    _name = 'res.sector'
    _description = 'Sector of Customer'

    name = fields.Char('Sector')
    code = fields.Char('code')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sector_id = fields.Many2one('res.sector','Sector')
    sectors_ids = fields.Many2many('res.sector','partner_sector_rel','res_sector_id','sector_id','Sectors')
    bool_postobon = fields.Boolean(default = False)
    bool_avon = fields.Boolean(default=False)

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if self.city_id:
            partners = len(self.search([('city_id', '=', self.city_id.id)]))
            self.ref = self.city_id.zipcode + str(partners)
            self.zip = self.ref

    lead_time = fields.Integer('Deal Lead Time')
    tolerance_minimal = fields.Integer('% Minimal Tolerance')
    tolerance_maximun = fields.Integer('% Maximun Tolerance')
    tolerance_minimal_day = fields.Integer('Minimal Tolerance Day')
    tolerance_maximun_day = fields.Integer('Maximun Tolerance Day')
    day_billing = fields.Integer('Days Billing Cut')
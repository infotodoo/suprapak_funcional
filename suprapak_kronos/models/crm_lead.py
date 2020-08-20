# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessDenied

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sheet_count = fields.Integer('Number of sheets', compute='_compute_sheet_data')
    sheet_ids = fields.One2many('data.sheet', 'opportunity_id', 'Sheets')
    currency_id = fields.Many2one('res.currency', 'Currency')
    product_code = fields.Char('Product code', help='Customer product code')
    sector_id = fields.Many2one('res.sector', 'Sector', compute = '_compute_sector')

    @api.depends('partner_id')
    def _compute_sector(self):
        if self.partner_id:
            self.sector_id = self.partner_id.sector_id.id
        else:
            self.sector_id = None

    def warning(self):
        if not self.currency_id :
            raise AccessDenied(("Debe seleccionar la moneda y el codigo del producto"))
        if not self.product_code :
            raise AccessDenied(("Debe seleccionar la moneda y el codigo del producto"))

    def _compute_sheet_data(self):
        for lead in self:
            count = len(lead.sheet_ids)
            lead.sheet_count = count

    def action_new_data_sheet(self):
        name = ''
        self.warning()
        if self.partner_id:
            name += self.partner_id.zip
        name += ' - ' + self.product_code
        action = self.env.ref("suprapak_kronos.action_new_data_sheet_new").read()[0]
        action['context'] = {
            'search_default_opportunity_id': self.id,
            'default_opportunity_id': self.id,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_team_id': self.team_id.id,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_currency_id': self.currency_id.id,
            'default_product_code': self.product_code,
            'default_name': name,
            'default_sector_id': self.sector_id.id,
        }
        return action

    def action_view_data_sheet(self):
        action = self.env.ref('suprapak_kronos.action_data_sheet').read()[0]
        action['context'] = {
            'default_partner_id': self.partner_id.id,
            'default_opportunity_id': self.id
        }
        action['domain'] = [('opportunity_id', '=', self.id)]
        return action


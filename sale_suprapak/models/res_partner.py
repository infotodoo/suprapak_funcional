from odoo import fields,models,api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    region = fields.Char('Region',related='country_id.region')
    sub_region = fields.Char('Sub-Region',related='country_id.sub_region')
    average_days = fields.Char('Average Days',related='country_id.average_days')
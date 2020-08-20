from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sheet_id = fields.Many2one('data.sheet', 'Data Sheet')
    residue = fields.Boolean('Residue')

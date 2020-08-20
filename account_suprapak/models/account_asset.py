from odoo import models,api,fields

class AccountAsset(models.Model):
    _inherit = 'account.asset'

    photo = fields.Binary('Photo')
    plaque = fields.Char('Plaque',required=True)
    stock_location_id = fields.Many2one('stock.location','Stock Location',tracking=True,required=True)
    assigned_id = fields.Many2one('hr.employee','Assigned to',tracking=True,required=True)

    _sql_constraints = [
        ('plaque_uniq', 'unique (plaque)', "A asset with the same plaque already exists."),
    ]
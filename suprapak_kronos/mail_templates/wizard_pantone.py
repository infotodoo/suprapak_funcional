from odoo import fields, models, api

class SelectPantone(models.TransientModel):
    _name = 'select.pantone'
    _description = 'Select Pantone'

    pantone_id = fields.Many2one('pantone.print','Pantone',required=True)

    #def action_pantone(self):
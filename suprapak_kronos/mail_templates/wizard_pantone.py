from odoo import fields, models, api

class SelectPantone(models.TransientModel):
    _name = 'select.pantone'
    _description = 'Select Pantone'

    pantone_id = fields.Many2one('pantone.print','Pantone',required=True)
    paticipation = fields.Float('Participation')
    bcm = fields.Float('BCM Pantone')

    def test(self):
        lines = []
        for line in self.pantone_id.color_ids:
            dic={
                'product_id':line.product_id.id,
                'participation_pantone': self.paticipation,
                'name_pantone': self.pantone_id.name,
                'standard_price': line.product_id.standard_price,
                'percentage': line.percentage,
                'bcm': self.bcm,
            }
            lines.append((0,0,dic))
            print_color_ids = self.env['data.sheet'].browse(self._context.get('active_id'))
            print_color_ids.write({'print_color_ids':lines})
        return True
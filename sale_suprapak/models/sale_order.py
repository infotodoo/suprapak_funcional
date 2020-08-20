from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_planned_finished = fields.Datetime('Date Finish Production', compute='_compute_date_planned_finished')

    def _compute_date_planned_finished(self):
        for record in self:
            date_planned_finished = False
            domain = [('origin', '=', record.name)]
            orders = self.env['mrp.production'].search(domain)
            for production in orders:
                date_planned_finished = production.date_planned_finished
            record.date_planned_finished = date_planned_finished

from odoo import fields,models,api

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    out = fields.Boolean(compute='_compute_out')
    exportation_billing = fields.Char('Number of Exportation Billing')
    logistic_operator_id = fields.Many2one('logistic.operator','Logistic Operator') 
    number_guide = fields.Char('Number of Guide')
    date_client = fields.Datetime('Datetime Delivery Customer')
    delivery_time = fields.Char('Delivery Time')

    def _compute_out(self):
        for record in self:
            if record.picking_type_id.warehouse_id.code == 'DES':
                record.out = True
            else:
                record.out = False
            
class LogisticOperator(models.Model):
    _name = 'logistic.operator'
    _description = 'This is the space to Logistic Operator'

    name = fields.Char('Name')
    code = fields.Char('Code')
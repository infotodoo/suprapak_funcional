from odoo import models, api, fields

class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget.lines'

    purchase_mount = fields.Float('Purchase Mount', compute="_compute_purchase_mount")
    copy_purchase = fields.Float(compute='_compute_copy_purchase',tracking=True)

    def _compute_copy_purchase(self):
        for record in self:
            record.copy_purchase = record.planned_amount

    def _compute_purchase_mount(self):
        for record in self:
            if record.general_budget_id:
                account_ids = record.general_budget_id.account_ids.ids
                purchase_ids = self.env['purchase.order.line'].search([('product_account','in',account_ids),
                ('date_planned','>=',record.date_from),('date_planned','<=',record.date_to)])
                total = 0
                dic =  {}
                dic['total'] = 0
                for purchase_obj in purchase_ids:
                    if purchase_obj.order_id.state == 'purchase':
                        if purchase_obj.product_account.id in account_ids:    
                            total += purchase_obj.price_subtotal
                            dic['total'] = total
                            dic['date'] = purchase_obj.date_planned
                record.purchase_mount = dic['total'] if dic['total'] else 0
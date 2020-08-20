from odoo import models,fields,api

class WizardPurchase(models.Model):
    _name = 'wizard.purchase'
    _description = 'This is the wizard for Purchase'

    message = fields.Char()
    users_ids = fields.Many2many('res.users','users_purchase_wizard_rel','purchase_id','user_id','Users')

    def action_create_activity(self):
        for record in self:
            purchase_id = self.env['purchase.order'].browse(self._context.get('active_id'))
            purchase_id.state = 'budget'
            model_id = self.env.ref('purchase.model_purchase_order')
            type_id = self.env.ref('mail.mail_activity_data_todo')
            summary = 'El pedido ha sido bloqueado por superar el presupuesto, por favor revisar'
            users = record.users_ids
            for user in users:
                activity_data = {
                    'res_id': purchase_id.id,
                    'res_model_id': model_id.id,
                    'activity_type_id': type_id.id,
                    'summary': summary,
                    'user_id': user.id,
                }
                self.env['mail.activity'].create(activity_data)
        return True
from odoo import api, fields, models


class ActivityCreateQuotation(models.TransientModel):
    _name = "data.revision"
    _description = 'wizard create revision buttom'

    message = fields.Text('observations')
    users_ids = fields.Many2many('res.users', 'users_revision_rel', 'revision_id', 'user_id', 'Users')

    def action_create_revision(self):
        for record in self:
            sheet_id = self.env['data.sheet'].browse(self._context.get('active_id'))
            model_id = self.env.ref('suprapak_kronos.model_data_sheet')
            type_id = self.env.ref('mail.mail_activity_data_todo')
            summary = record.message
            users = record.users_ids
            for user in users:
                activity_data = {
                    'res_id': sheet_id.id,
                    'res_model_id': model_id.id,
                    'activity_type_id': type_id.id,
                    'summary': summary,
                    'user_id': user.id,
                }
                ma = self.env['mail.activity'].sudo().create(activity_data)
                print(ma.id)
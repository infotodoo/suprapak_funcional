from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.http import request


class SaleCompany(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals_list):
        result= super(SaleCompany, self).create(vals_list)
        if result.company_id != self.env.company:
            if 'key' not in request.session:
                request.session.update({'key' : 'Keys'})
                raise UserError(_('You are creating a quotation in a company different from  where you are from. \n Do you want to Continue ?'))
        request.session.pop('key', None)
        if result.opportunity_id:
            attachments = self.env['ir.attachment'].search([('res_id','=',result.opportunity_id.id)])
            if attachments:
                for attachment in attachments:
                    self.env['ir.attachment'].create({
                        'name' : attachment.name,
                        'description' : attachment.description,
                        'res_model' : 'sale.order',
                        'res_field' : attachment.res_field,
                        'res_id' : result.id,
                        'company_id' : attachment.company_id.id,
                        'type' : attachment.type,
                        'url' : attachment.url,
                        'public' : attachment.public,
                        'access_token' : attachment.access_token,
                        'store_fname' : attachment.store_fname,
                        'file_size' :attachment.file_size,
                        'checksum' : attachment.checksum,
                        'mimetype' : attachment.mimetype,
                        'index_content' : attachment.index_content

                    })
        return result
    def action_confirm(self):
        super(SaleCompany, self).action_confirm()
        if self.opportunity_id:
            attachments = self.env['ir.attachment'].search([('res_id','=',self.opportunity_id.id)])
            if attachments:
                for attachment in attachments:
                    for line in self.order_line:
                        if line.task_id:
                            self.env['ir.attachment'].create({
                                'name': attachment.name,
                                'description': attachment.description,
                                'res_model': 'project.task',
                                'res_field': attachment.res_field,
                                'res_id': line.task_id.id,
                                'company_id': attachment.company_id.id,
                                'type': attachment.type,
                                'url': attachment.url,
                                'public': attachment.public,
                                'access_token': attachment.access_token,
                                'store_fname': attachment.store_fname,
                                'file_size': attachment.file_size,
                                'checksum': attachment.checksum,
                                'mimetype': attachment.mimetype,
                                'index_content': attachment.index_content

                            })
                        elif line.project_id:
                            self.env['ir.attachment'].create({
                                'name': attachment.name,
                                'description': attachment.description,
                                'res_model': 'project.project',
                                'res_field': attachment.res_field,
                                'res_id': line.project_id.id,
                                'company_id': attachment.company_id.id,
                                'type': attachment.type,
                                'url': attachment.url,
                                'public': attachment.public,
                                'access_token': attachment.access_token,
                                'store_fname': attachment.store_fname,
                                'file_size': attachment.file_size,
                                'checksum': attachment.checksum,
                                'mimetype': attachment.mimetype,
                                'index_content': attachment.index_content

                            })
